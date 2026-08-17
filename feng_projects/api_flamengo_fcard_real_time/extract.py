import logging
import time
import os 
import pandas as pd
import requests

from datetime import datetime, timedelta
from urllib.parse import urlencode
from unidecode import unidecode
from auth_fcard import get_headers
from utils import connect_dw_prod
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("FCARD_API_URL")

def retry_request(url, max_retries=5, wait_seconds=10):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                url,
                headers=get_headers(),
                timeout=60
            )

            if response.status_code == 200:
                return response

            logging.warning(
                f"[EXTRACT][REQUEST] tentativa={attempt}/{max_retries} | status={response.status_code}"
            )
            time.sleep(wait_seconds)

        except requests.exceptions.RequestException as error:
            logging.error(
                f"[EXTRACT][REQUEST] tentativa={attempt}/{max_retries} | erro={error}"
            )
            time.sleep(wait_seconds)

    raise RuntimeError(f"Falha após {max_retries} tentativas: {url}")


def normalizar_texto(valor):
    if pd.isna(valor):
        return ""

    return unidecode(str(valor).strip().upper())


def classificar_tipo_evento(match):
    match_norm = normalizar_texto(match)

    if "ESTACIONAMENTO" in match_norm:
        return "ESTACIONAMENTO"

    if "ESPACO" in match_norm or "FLA+" in match_norm or "FLA PLUS" in match_norm:
        return "FLA_PLUS"

    return "JOGO"


def formatar_data_eventos(data_yyyy_mm_dd):
    return datetime.strptime(data_yyyy_mm_dd, "%Y-%m-%d").strftime("%d/%m/%Y")


def formatar_data_tickets(data_yyyy_mm_dd, horario):
    data = datetime.strptime(data_yyyy_mm_dd, "%Y-%m-%d").strftime("%d/%m/%Y")
    return f"{data} {horario}"


def extrair_eventos_por_periodo(start_date, end_date):
    params = {
        "start_date": formatar_data_eventos(start_date),
        "end_date": formatar_data_eventos(end_date),
    }

    url = f"{BASE_URL}/ws/events?{urlencode(params)}"

    response = retry_request(url)
    data = response.json()

    if isinstance(data, dict):
        events = data.get("events", [])
    elif isinstance(data, list):
        events = data
    else:
        raise ValueError(f"Formato inesperado em events: {type(data)}")

    df_events = pd.DataFrame(events)

    if df_events.empty:
        return df_events

    df_events.columns = df_events.columns.str.strip().str.lower()

    df_events["stadium_norm"] = df_events["stadium"].apply(normalizar_texto)

    df_events = df_events[
        df_events["stadium_norm"].str.contains("MARACANA", na=False)
    ]

    # resto igual
    df_events["event_id"] = df_events["event_id"].astype(str)

    df_events["event_date_iso"] = pd.to_datetime(
        df_events["event_date"],
        format="%d/%m/%Y",
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    df_events["match_norm"] = df_events["match"].apply(normalizar_texto)
    df_events["championship_norm"] = df_events["championship"].apply(normalizar_texto)

    df_events["tipo_evento"] = df_events["match"].apply(classificar_tipo_evento)

    df_events = filtrar_eventos_validos(df_events)

    return df_events


# ===========================================
# EXTRACT EVENTS POR DATAS JOGO
# ===========================================

def extrair_eventos_por_datas_jogo(
    datas_jogo
):

    dfs = []

    for data_jogo in datas_jogo:

        df_temp = extrair_eventos_por_periodo(
            start_date=data_jogo,
            end_date=data_jogo
        )

        if (
            df_temp is not None
            and not df_temp.empty
        ):

            dfs.append(df_temp)

    if not dfs:

        logging.warning(
            f"[EXTRACT] eventos=0 | datas={datas_jogo}"
        )

        return pd.DataFrame()

    df_events = pd.concat(
        dfs,
        ignore_index=True
    )

    df_events = df_events.drop_duplicates(
        subset=["event_id"]
    )

    df_events = definir_evento_jogo_base(
        df_events
    )

    logging.info(
        f"[EXTRACT] eventos={len(df_events)} "
        f"| {df_events['tipo_evento'].value_counts(dropna=False).to_dict()}"
    )

    return df_events


def extrair_eventos_30_dias():
    conn = connect_dw_prod()

    with conn.connect() as sql:
        result = sql.execute(text("""
            select max(dt_evento::timestamp)
            from dw_prd_flamengo.dm_mkt.fcard_eventos
            where dt_evento <= current_date()
            and upper(partida) like 'FLAMENGO%'
        """)).fetchone()

        data_base = result[0]

    if data_base is None:
        logging.warning("[EXTRACT] sem jogo base Flamengo")
        return pd.DataFrame()

    data_inicio = data_base.strftime("%Y-%m-%d")
    data_fim = (data_base + timedelta(days=30)).strftime("%Y-%m-%d")

    logging.info(f"[EXTRACT] events +30 dias (base Flamengo) | {data_inicio} → {data_fim}")

    df_events = extrair_eventos_por_periodo(
        start_date=data_inicio,
        end_date=data_fim
    )

    if df_events.empty:
        return df_events

    df_events = definir_evento_jogo_base(df_events)

    return df_events


def filtrar_eventos_validos(df_events):
    df_events = df_events.copy()

    df_events = df_events[df_events["championship_norm"] != "NBB"]

    df_events = df_events[
        ~df_events["championship_norm"].str.contains(
            "TESTE|PACOTE|FUTEBOLCARD|TREINO|BCLA|COPA FLA MARACA|FLA FEST",
            na=False
        )
    ]

    df_events = df_events[
        ~df_events["match_norm"].str.contains(
            "TESTE|PACOTE",
            na=False
        )
    ]

    return df_events


def definir_evento_jogo_base(df_events):
    if df_events.empty:
        return df_events

    df_events = df_events.copy()
    df_events["event_id_int"] = df_events["event_id"].astype(int)

    df_events["event_id_jogo_base"] = None
    df_events["partida_base"] = None

    for _, grupo in df_events.groupby(["event_date", "event_time"]):
        jogos = grupo[grupo["tipo_evento"] == "JOGO"]

        if not jogos.empty:
            evento_base = jogos.sort_values("event_id_int").iloc[0]
        else:
            evento_base = grupo.sort_values("event_id_int").iloc[0]

        df_events.loc[grupo.index, "event_id_jogo_base"] = evento_base["event_id"]
        df_events.loc[grupo.index, "partida_base"] = evento_base["match"]

    df_events = df_events.drop(columns=["event_id_int"])

    return df_events


def extrair_tickets_por_evento(event_id, start_datetime, end_datetime):
    params = {
        "event": event_id,
        "start_date": start_datetime,
        "end_date": end_datetime,
    }

    url = f"{BASE_URL}/ws/tickets?{urlencode(params)}"

    response = retry_request(url)
    data = response.json()

    if isinstance(data, dict) and "tickets" in data:
        tickets = data["tickets"]

    elif (
        isinstance(data, list)
        and len(data) > 0
        and isinstance(data[0], dict)
        and "tickets" in data[0]
    ):
        tickets = data[0]["tickets"]

    elif isinstance(data, list):
        tickets = data

    else:
        raise ValueError(f"Formato inesperado em tickets do evento {event_id}: {type(data)}")

    return pd.DataFrame(tickets)


def montar_df_tickets(df_events, start_datetime, end_datetime):
    if df_events.empty:
        logging.warning("[EXTRACT] tickets=0 | nenhum evento recebido")
        return pd.DataFrame()

    dfs_tickets = []

    for _, evento in df_events.iterrows():
        event_id = evento["event_id"]
        tipo_evento = evento["tipo_evento"]

        df_tickets = extrair_tickets_por_evento(
            event_id=event_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )

        logging.info(f"[EXTRACT] {event_id} | {tipo_evento} | {len(df_tickets)}")

        if df_tickets.empty:
            continue

        df_tickets["event_id_original"] = evento["event_id"]
        df_tickets["event_id_jogo_base"] = evento["event_id_jogo_base"]
        df_tickets["tipo_evento"] = evento["tipo_evento"]

        df_tickets["event_date"] = evento["event_date"]
        df_tickets["event_date_iso"] = evento["event_date_iso"]
        df_tickets["event_time"] = evento["event_time"]
        df_tickets["match"] = evento["match"]
        df_tickets["partida_base"] = evento["partida_base"]
        df_tickets["championship"] = evento["championship"]
        df_tickets["stadium"] = evento.get("stadium", None)

        dfs_tickets.append(df_tickets)

    if not dfs_tickets:
        logging.warning("[EXTRACT] tickets=0 | nenhum ticket encontrado")
        return pd.DataFrame()

    dfs_tickets = [
        df for df in dfs_tickets
        if df is not None and not df.empty
    ]

    if dfs_tickets:
        df_final = pd.concat(
            dfs_tickets,
            ignore_index=True
        )
    else:
        df_final = pd.DataFrame()

    logging.info(
        f"[EXTRACT] total={len(df_final)} | {df_final['tipo_evento'].value_counts(dropna=False).to_dict()}"
    )

    return df_final


def extrair_clients_por_tickets(df_tickets):
    if df_tickets.empty:
        return pd.DataFrame()

    dfs = []

    # CPF (única forma válida)
    if "cpf" in df_tickets.columns:
        cpfs = (
            df_tickets["cpf"]
            .dropna()
            .astype(str)
            .str.replace(r"\D", "", regex=True)
            .loc[lambda s: s != ""]
            .loc[lambda s: s != "-1"]
            .drop_duplicates()
            .tolist()
        )
    else:
        cpfs = []

    for cpf in cpfs:
        url = f"{BASE_URL}/ws/clients?cpf={cpf}"

        response = retry_request(url)
        data = response.json()

        if isinstance(data, list) and data:
            dfs.append(pd.json_normalize(data))

    if not dfs:
        logging.warning("[EXTRACT] clients=0")
        return pd.DataFrame()

    df_clients = pd.concat(dfs, ignore_index=True)

    logging.info(f"[EXTRACT] clients={len(df_clients)}")

    return df_clients


def extract_reprocessamento(datas_jogo):

    # EVENTS
    df_events = extrair_eventos_por_datas_jogo(datas_jogo)
    df_events = definir_evento_jogo_base(df_events)

    if df_events.empty:
        logging.warning("[EXTRACT] reprocessamento | nenhum evento válido")
        return {
            "events": pd.DataFrame(),
            "tickets": pd.DataFrame(),
            "clients": pd.DataFrame(),
        }

    # RANGE GLOBAL (mesmo padrão que você já usa)
    start_datetime = "01/01/2020 00:00"
    end_datetime = "31/12/2026 23:59"

    # TICKETS
    df_tickets = montar_df_tickets(
        df_events=df_events,
        start_datetime=start_datetime,
        end_datetime=end_datetime
    )

    # CLIENTS (novo)
    df_clients = extrair_clients_por_tickets(df_tickets)

    logging.info(
        f"[EXTRACT] final | tickets={len(df_tickets)} | clients={len(df_clients)}"
    )

    return {
        "events": df_events,
        "tickets": df_tickets,
        "clients": df_clients,
    }


def extract_real_time(start_datetime, end_datetime, eventos_ids):

    logging.info(
        f"[EXTRACT][REALTIME] "
        f"start={start_datetime} | "
        f"end={end_datetime} | "
        f"eventos={eventos_ids}"
    )

    # ===========================================
    # BUSCA TODOS EVENTOS
    # ===========================================
    df_events = extrair_eventos_por_periodo(
        start_date="2000-01-01",
        end_date="2100-01-01"
    )

    if df_events.empty:
        logging.warning("[EXTRACT][REALTIME] nenhum evento retornado")
        return pd.DataFrame()

    # ===========================================
    # FILTRA EVENTOS DO REALTIME
    # ===========================================
    df_events["event_id"] = df_events["event_id"].astype(str)

    eventos_ids = [str(x) for x in eventos_ids]

    df_events = df_events[
        df_events["event_id"].isin(eventos_ids)
    ].copy()

    if df_events.empty:
        logging.warning(
            f"[EXTRACT][REALTIME] "
            f"eventos não encontrados={eventos_ids}"
        )
        return pd.DataFrame()

    # ===========================================
    # DEFINE EVENTO BASE
    # ===========================================
    df_events = definir_evento_jogo_base(df_events)

    logging.info(
        "[EXTRACT][REALTIME] eventos carregados | "
        f"total={len(df_events)} | "
        f"resumo={df_events['tipo_evento'].value_counts(dropna=False).to_dict()}"
    )

    # ===========================================
    # FORMATA DATAS PARA API
    # ===========================================
    start_ticket = start_datetime.strftime("%d/%m/%Y %H:%M")

    end_ticket = end_datetime.strftime("%d/%m/%Y %H:%M")

    logging.info(
        f"[EXTRACT][REALTIME] janela tickets="
        f"{start_ticket} → {end_ticket}"
    )

    # ===========================================
    # MONTA DF TICKETS
    # ===========================================
    df_final = montar_df_tickets(
        df_events=df_events,
        start_datetime=start_ticket,
        end_datetime=end_ticket
    )

    if df_final.empty:
        logging.warning(
            "[EXTRACT][REALTIME] nenhum ticket encontrado"
        )
        return df_final

    # ===========================================
    # AJUSTE DATA PAGAMENTO
    # ===========================================
    if "payment_date" in df_final.columns:

        df_final["payment_date_dt"] = pd.to_datetime(
            df_final["payment_date"],
            format="%d/%m/%Y %H:%M",
            errors="coerce"
        )

    # ===========================================
    # LOG FINAL
    # ===========================================
    logging.info(
        "[EXTRACT][REALTIME] final | "
        f"linhas={len(df_final)} | "
        f"resumo={df_final['tipo_evento'].value_counts(dropna=False).to_dict()}"
    )

    return df_final