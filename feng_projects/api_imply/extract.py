import os
import json
import logging
import requests
import pandas as pd

from datetime import datetime, timedelta
from requests.exceptions import HTTPError, ReadTimeout


def extracao_datalake_vasco(date_start: str, date_end: str, max_results: int) -> pd.DataFrame:
    auth = os.getenv("AUTHORIZATION_VASCO")
    if not auth:
        raise ValueError("AUTHORIZATION_VASCO não encontrado nas variáveis de ambiente")

    url = "https://vascoadmin.eleventickets.com/dataLakeVasco"
    headers = {"Authorization": auth}

    # +1 no date_end para pegar o dia final inteiro (fim exclusivo)
    date_end_api = (
        datetime.strptime(date_end, "%Y-%m-%d") + timedelta(days=1)
    ).strftime("%Y-%m-%d")

    timeout_s = 180

    # ---------------------------
    # ETAPA 1: extrair por dthr_reserva e coletar idapresentacao distintos
    # ---------------------------
    page = 1
    all_rows_1 = []

    while True:
        params = {
            "page": page,
            "max_results": max_results,
            "dthr_reserva_ini": date_start,
            "dthr_reserva_fim": date_end_api,
        }

        logging.info(f"🟡 [VASCO] - ETAPA 1 - page={page} max_results={max_results}")

        try:
            resp = requests.post(url, headers=headers, params=params, timeout=timeout_s)
            resp.raise_for_status()
        except ReadTimeout:
            logging.exception(f"🟡 [VASCO] - ETAPA 1 - Timeout page={page}")
            raise
        except HTTPError:
            logging.exception(f"🟡 [VASCO] - ETAPA 1 - HTTP error page={page} status={resp.status_code}")
            raise

        payload = resp.json()

        # Envelope: {'id','error','result'}
        if isinstance(payload, dict) and "result" in payload:
            if payload.get("error"):
                raise ValueError(f"API retornou error={payload.get('error')}")

            result = payload["result"]
            if isinstance(result, dict):
                payload = result
            elif isinstance(result, str):
                payload = json.loads(result)  # só funciona se vier JSON válido
            else:
                raise ValueError(f"Tipo inesperado em payload['result']: {type(result)}")

        # Esperado: {'rows': [...]}
        if not (isinstance(payload, dict) and "rows" in payload):
            raise ValueError(
                f"Formato inesperado (ETAPA 1). type={type(payload)} "
                f"keys={list(payload.keys()) if isinstance(payload, dict) else None}"
            )

        rows = payload["rows"]
        if not rows:
            logging.info(f"🟡 [VASCO] - ETAPA 1 - Página {page} sem rows. Encerrando.")
            break

        all_rows_1.extend(rows)

        if len(rows) < max_results:
            logging.info(f"🟡 [VASCO] - ETAPA 1 - Página {page} retornou {len(rows)}.")
            break

        page += 1

    all_rows_1 = [r if isinstance(r, dict) else {"_raw": r} for r in all_rows_1]
    df_1 = pd.DataFrame(all_rows_1)

    if "idapresentacao" not in df_1.columns:
        raise ValueError("Coluna 'idapresentacao' não existe no retorno da ETAPA 1")

    df_idapresentacao = (
        df_1[["idapresentacao"]]
        .dropna()
        .astype({"idapresentacao": "string"})
        .drop_duplicates()
        .reset_index(drop=True)
    )

    logging.info(f"🟡 [VASCO] - ETAPA 1 - idapresentacao distintos: {len(df_idapresentacao)}")

    # ---------------------------
    # ETAPA 2: para cada idapresentacao, extrair tudo pelo endpoint e consolidar
    # ---------------------------
    all_rows_2 = []

    for i, idapresentacao in enumerate(df_idapresentacao["idapresentacao"].tolist(), start=1):
        page2 = 1

        while True:
            params2 = {
                "page": page2,
                "max_results": max_results,
                "idapresentacao": idapresentacao,
            }

            logging.info(
                f"🟡 [VASCO] - ETAPA 2 - idapresentacao {i}/{len(df_idapresentacao)} "
                f"- page={page2} max_results={max_results}"
            )

            try:
                resp2 = requests.post(url, headers=headers, params=params2, timeout=timeout_s)
                resp2.raise_for_status()
            except ReadTimeout:
                logging.exception(f"🟡 [VASCO] - ETAPA 2 - Timeout idapresentacao={idapresentacao} page={page2}")
                raise
            except HTTPError:
                logging.exception(
                    f"🟡 [VASCO] - ETAPA 2 - HTTP error idapresentacao={idapresentacao} page={page2} status={resp2.status_code}"
                )
                raise

            payload2 = resp2.json()

            if isinstance(payload2, dict) and "result" in payload2:
                if payload2.get("error"):
                    raise ValueError(f"API retornou error={payload2.get('error')}")

                result2 = payload2["result"]
                if isinstance(result2, dict):
                    payload2 = result2
                elif isinstance(result2, str):
                    payload2 = json.loads(result2)  # só funciona se vier JSON válido
                else:
                    raise ValueError(f"Tipo inesperado em payload['result']: {type(result2)}")

            if not (isinstance(payload2, dict) and "rows" in payload2):
                raise ValueError(
                    f"Formato inesperado (ETAPA 2). type={type(payload2)} "
                    f"keys={list(payload2.keys()) if isinstance(payload2, dict) else None}"
                )

            rows2 = payload2["rows"]
            if not rows2:
                break

            all_rows_2.extend(rows2)

            if len(rows2) < max_results:
                break

            page2 += 1

    all_rows_2 = [r if isinstance(r, dict) else {"_raw": r} for r in all_rows_2]
    df_2 = pd.DataFrame(all_rows_2)

    df_2["dedupe_key"] = df_2.apply(
        lambda r: r["idacesso"]
        if pd.notna(r.get("idacesso"))
        else f"{r.get('idapresentacao', '')}|{r.get('codigo', '')}",
        axis=1,
    )

    df_2 = df_2.drop_duplicates(subset=["dedupe_key"], keep="first").drop(columns=["dedupe_key"])

    df_2 = df_2.drop(columns=["_raw"], errors="ignore")

    # df_2.to_csv("vasco_por_idapresentacao.csv", index=False, encoding="utf-8")
    return df_2

