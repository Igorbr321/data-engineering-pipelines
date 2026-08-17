import logging
import requests
import pandas as pd

from datetime import datetime, timedelta
from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError
from requests import HTTPError
from common.authenticator_prd import get_token_prd_base64

BASE_URL = "https://api.esm.com.br"
SERVICE_PATH_USERS = "nsuser"
CSV_OUT = "teste_users.csv"


# =========================
# TRATANDO COLUNAS 
# =========================

def _addresses_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "addresses"
    if df.empty or col not in df.columns:
        return df

    addr = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    addr_df = pd.json_normalize(addr).add_prefix("addresses_")
    return pd.concat([df.drop(columns=[col]), addr_df], axis=1)


def _active_addresses_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "activeAddresses"
    if df.empty or col not in df.columns:
        return df

    addr = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    addr_df = pd.json_normalize(addr).add_prefix("active_addresses_")
    return pd.concat([df.drop(columns=[col]), addr_df], axis=1)


def _person_phones_columns(df: pd.DataFrame) -> pd.DataFrame:
    col = "person.phones"
    if df.empty or col not in df.columns:
        return df

    phones = df[col].apply(lambda x: x[0] if isinstance(x, list) and x else {})
    phones_df = pd.json_normalize(phones).add_prefix("person_phones_")
    return pd.concat([df.drop(columns=[col]), phones_df], axis=1)


# =======================================
# TRANSFORMANDO E NORMALIZANDO
# =======================================

def tratar_users(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    df = _addresses_columns(df)
    df = _active_addresses_columns(df)
    df = _person_phones_columns(df)

    # NÃO reordena colunas
    return df


def normalizar_colunas_usuarios(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    df = df.copy()
    cols = df.columns.astype(str)

    cols = cols.str.replace(".", "_", regex=False)
    cols = cols.str.replace(r"(.)([A-Z][a-z]+)", r"\1_\2", regex=True)
    cols = cols.str.replace(r"([a-z0-9])([A-Z])", r"\1_\2", regex=True)

    cols = cols.str.lower()
    cols = cols.str.replace(r"__+", "_", regex=True).str.strip("_")

    cols = cols.str.replace(r"^updates_dates_", "updates_", regex=True)
    cols = cols.str.replace(r"^addresses_", "address_", regex=True)
    cols = cols.str.replace(r"^active_addresses_", "active_address_", regex=True)
    cols = cols.str.replace(r"^person_phones_", "phone_", regex=True)

    df.columns = cols
    return df


def transformar_users(df: pd.DataFrame) -> pd.DataFrame:

    df = tratar_users(df)
    df = normalizar_colunas_usuarios(df)
    df.columns = df.columns.str.upper()

    return df


# =========================
# EXTRAÇÃO
# =========================

def extracao_usuarios(date_start: str, date_end: str, per_page: int) -> pd.DataFrame:
    date_end_api = (
        datetime.strptime(date_end, "%Y-%m-%d").date() + timedelta(days=1)
    ).strftime("%Y-%m-%d")

    logging.info(f"🟡 [USERS] - Período: {date_start} -> {date_end}")

    base_url = f"{BASE_URL}/{SERVICE_PATH_USERS}"

    page = 1
    total_pages = None
    todos_registros: list[dict] = []

    readtimeout_tentativas = 0
    MAX_RETRY_READTIMEOUT = 2

    while True:
        if total_pages is not None and page > total_pages:
            break

        params = {
            "date_start": date_start,
            "date_end": date_end_api,
            "per_page": per_page,
            "page": page,
        }

        try:
            token_b64 = get_token_prd_base64()
            headers = {"Authorization": f"Bearer {token_b64}"}

            resp = requests.get(base_url, headers=headers, params=params, timeout=60)
            resp.raise_for_status()
            payload = resp.json() if resp.text else {}

            # resetou porque deu certo
            readtimeout_tentativas = 0

        except (ReadTimeout, ReadTimeoutError):
            readtimeout_tentativas += 1
            logging.warning(
                f"🟡 [USERS] - ReadTimeout na página {page} "
                f"(tentativa {readtimeout_tentativas}/{MAX_RETRY_READTIMEOUT})"
            )

            if readtimeout_tentativas >= MAX_RETRY_READTIMEOUT:
                logging.warning(
                    f"🟡 [USERS] - Estouro de ReadTimeout na página {page}. Seguindo para a próxima."
                )
                readtimeout_tentativas = 0
                page += 1

            continue

        except HTTPError as e:
            status = getattr(e.response, "status_code", None)
            if status == 500:
                logging.warning(
                    f"🟡 [USERS] - HTTP 500 na página {page}. Pulando para a próxima."
                )
                page += 1
                continue
            raise

        if page == 1:
            pagination = payload.get("pagination") or {}
            total_pages = pagination.get("pages")
            logging.info(
                f"🟡 [USERS] - Total de páginas retornadas pela API: {total_pages}"
            )

        registros = payload.get("users") or payload.get("data") or []
        logging.info(
            f"🟡 [USERS] - Página {page}/{total_pages} - registros: {len(registros)}"
        )

        if registros:
            todos_registros.extend(registros)

        page += 1

    df = pd.json_normalize(todos_registros) if todos_registros else pd.DataFrame()
    return transformar_users(df)


