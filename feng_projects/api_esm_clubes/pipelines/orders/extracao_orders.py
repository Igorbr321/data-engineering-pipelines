import json
import logging
import requests
import time
import pandas as pd

from datetime import datetime, timedelta
from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError
from requests import HTTPError
from common.authenticator_prd import get_token_prd_base64

BASE_URL = "https://api.esm.com.br"
SERVICE_PATH_ORDERS = "nsorder"
CSV_OUT = "teste_orders.csv"

# =========================
# TRATANDO COLUNAS 
# =========================

def _payments_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "payments"
    if df.empty or col not in df.columns:
        return df

    pay = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    pay_df = pd.json_normalize(pay).add_prefix("payments_")
    return pd.concat([df.drop(columns=[col]), pay_df], axis=1)


def _statuses_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "statuses"
    if df.empty or col not in df.columns:
        return df

    sts = df[col].apply(lambda x: x[-1] if isinstance(x, list) and x else {})
    sts_df = pd.json_normalize(sts).add_prefix("statuses_")
    return pd.concat([df.drop(columns=[col]), sts_df], axis=1)


def _shippings_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "shippings"
    if df.empty or col not in df.columns:
        return df

    ship = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    ship_df = pd.json_normalize(ship).add_prefix("shippings_")
    return pd.concat([df.drop(columns=[col]), ship_df], axis=1)


def _shippings_products_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "shippings_products"
    if df.empty or col not in df.columns:
        return df

    prod = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    prod_df = pd.json_normalize(prod).add_prefix("shippings_products_")
    return pd.concat([df.drop(columns=[col]), prod_df], axis=1)


def _shippings_products_custom_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "shippings_products_custom"
    if df.empty or col not in df.columns:
        return df

    custom = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    custom_df = pd.json_normalize(custom).add_prefix("shippings_products_custom_")
    return pd.concat([df.drop(columns=[col]), custom_df], axis=1)


def _shippings_products_stamps_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "shippings_products_stamps"
    if df.empty or col not in df.columns:
        return df

    stamps = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    stamps_df = pd.json_normalize(stamps).add_prefix("shippings_products_stamps_")
    return pd.concat([df.drop(columns=[col]), stamps_df], axis=1)


def _shippings_products_all_configurations_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "shippings_products_allConfigurations"
    if df.empty or col not in df.columns:
        return df

    conf = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    conf_df = pd.json_normalize(conf).add_prefix("shippings_products_all_configurations_")
    return pd.concat([df.drop(columns=[col]), conf_df], axis=1)


def _benefit_promotions_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "benefit.promotions"
    if df.empty or col not in df.columns:
        return df

    promo = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    promo_df = pd.json_normalize(promo).add_prefix("benefit_promotions_")
    return pd.concat([df.drop(columns=[col]), promo_df], axis=1)

# ==================================================
# TRANSFORMANDO E NORMALIZANDO
# ==================================================

def tratar_orders(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    df = _payments_columns(df)
    df = _statuses_columns(df)
    df = _shippings_columns(df)
    df = _shippings_products_columns(df)
    df = _shippings_products_custom_columns(df)
    df = _benefit_promotions_columns(df)
    df = _shippings_products_stamps_columns(df)
    df = _shippings_products_all_configurations_columns(df)

    return df


def normalizar_colunas_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nomes de colunas automaticamente:
    - remove sufixos (_m999, _x, _y) no final
    - '.' -> '_'
    - camelCase / PascalCase -> snake_case
    - tudo minúsculo
    - evita '__'
    """
    if df is None or df.empty:
        return df

    df = df.copy()
    cols = df.columns.astype(str).str.strip()

    cols = cols.str.replace(r"(_m\d+|_x|_y)$", "", regex=True)
    cols = cols.str.replace(".", "_", regex=False)

    cols = cols.str.replace(r"(.)([A-Z][a-z]+)", r"\1_\2", regex=True)
    cols = cols.str.replace(r"([a-z0-9])([A-Z])", r"\1_\2", regex=True)

    cols = cols.str.lower()
    cols = cols.str.replace(r"__+", "_", regex=True).str.strip("_")

    df.columns = cols
    return df


def tipar_orders_snowflake(df: pd.DataFrame) -> pd.DataFrame:
    """
    - converte NaN/NA -> None (NULL real)
    - converte list/dict/tuple/set -> JSON string (evita erro no insert)
    """
    if df is None or df.empty:
        return df

    df = df.copy()

    df = df.replace({pd.NA: None})
    df = df.where(df.notna(), None)

    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].apply(
                lambda v: json.dumps(v, ensure_ascii=False)
                if isinstance(v, (list, dict, tuple, set))
                else v
            )

    df = df.where(df.notna(), None)
    return df


def transformar_orders(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    df = tratar_orders(df)
    df = normalizar_colunas_orders(df)
    df = tipar_orders_snowflake(df)

    # garante colunas como string antes do .str
    df.columns = df.columns.map(str).str.upper()

    return df


# =========================
# EXTRAÇÃO 
# =========================

def extracao_orders(date_start: str, date_end: str, per_page: int) -> pd.DataFrame:
    date_end_api = (
        datetime.strptime(date_end, "%Y-%m-%d").date() + timedelta(days=1)
    ).strftime("%Y-%m-%d")

    logging.info(f"🟢 [ORDERS] - Período: {date_start} -> {date_end}")

    base_url = f"{BASE_URL}/{SERVICE_PATH_ORDERS}"
    todos_registros: list[dict] = []

    page = 1
    total_pages = None

    MAX_RETRY_READTIMEOUT = 3
    BACKOFF_SECONDS = 5
    REQUEST_TIMEOUT = 120

    token_b64 = get_token_prd_base64()
    headers = {"Authorization": f"Bearer {token_b64}"}

    with requests.Session() as session:
        session.headers.update(headers)

        while True:
            if total_pages is not None and page > total_pages:
                break

            params = {
                "date_start": date_start,
                "date_end": date_end_api,
                "per_page": per_page,
                "page": page,
            }

            payload = None

            for tentativa in range(1, MAX_RETRY_READTIMEOUT + 1):
                try:
                    resp = session.get(
                        base_url,
                        params=params,
                        timeout=REQUEST_TIMEOUT
                    )
                    resp.raise_for_status()

                    if not resp.text:
                        payload = {}
                    else:
                        payload = resp.json()

                    break

                except (ReadTimeout, ReadTimeoutError):
                    logging.warning(
                        f"🟡 [ORDERS] - ReadTimeout na página {page} "
                        f"(tentativa {tentativa}/{MAX_RETRY_READTIMEOUT})"
                    )

                    if tentativa == MAX_RETRY_READTIMEOUT:
                        raise RuntimeError(
                            f"Falha definitiva por ReadTimeout na página {page}. "
                            f"Extração interrompida para não perder dados."
                        )

                    time.sleep(BACKOFF_SECONDS * tentativa)

                except requests.exceptions.JSONDecodeError as e:
                    raise RuntimeError(
                        f"Resposta inválida da API na página {page}: JSON malformado."
                    ) from e

                except HTTPError as e:
                    status = getattr(e.response, "status_code", None)
                    body = getattr(e.response, "text", "")

                    raise RuntimeError(
                        f"Erro HTTP na página {page}. Status: {status}. "
                        f"Resposta: {body[:500]}"
                    ) from e

                except requests.RequestException as e:
                    raise RuntimeError(
                        f"Erro de conexão na página {page}: {str(e)}"
                    ) from e

            if payload is None:
                raise RuntimeError(
                    f"Não foi possível obter payload da página {page}."
                )

            pagination = payload.get("pagination") or {}

            if page == 1:
                total_pages = pagination.get("pages")

                if total_pages is None:
                    raise RuntimeError(
                        "A API não retornou 'pagination.pages' na primeira página. "
                        "Não é seguro continuar a extração."
                    )

                try:
                    total_pages = int(total_pages)
                except (TypeError, ValueError) as e:
                    raise RuntimeError(
                        f"Valor inválido para total_pages retornado pela API: {total_pages}"
                    ) from e

                logging.info(
                    f"🟢 [ORDERS] - Total de páginas retornadas pela API: {total_pages}"
                )

                if total_pages <= 0:
                    logging.info("🟢 [ORDERS] - Nenhuma página retornada pela API.")
                    break

            registros = payload.get("orders") or payload.get("data") or []

            if not isinstance(registros, list):
                raise RuntimeError(
                    f"Estrutura inválida na página {page}: 'orders' não é lista."
                )

            logging.info(
                f"🟢 [ORDERS] - Página {page}/{total_pages} - registros: {len(registros)}"
            )

            if registros:
                todos_registros.extend(registros)

            page += 1

    df = pd.json_normalize(todos_registros) if todos_registros else pd.DataFrame()

    df.to_csv(CSV_OUT, index=False, encoding="utf-8-sig")
    return transformar_orders(df)











