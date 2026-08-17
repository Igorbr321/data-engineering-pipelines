import logging
import time

import pandas as pd

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import text

from utils import connect_dw_prod

from extract import (
    extract_real_time,
    extrair_eventos_30_dias,
    extrair_eventos_por_datas_jogo,
    extrair_eventos_por_periodo,
    definir_evento_jogo_base,
    montar_df_tickets,
    extrair_clients_por_tickets,

)

from transform import (
    transformar_events,
    transformar_tickets,
    transformar_clients,
)

from load import (
    load_events,
    load_clients,
    load_tickets_stg,
    load_dim_partida,
    load_ft_compraingresso,
    load_cogny_ticket_integration,
    load_realtime
)


TIMEZONE = ZoneInfo("America/Sao_Paulo")


# ===========================================
# REPROCESSAMENTO MANUAL
# ===========================================

def executar_reprocessamento_manual():

    datas_jogo = [
        "2026-05-20",
        # "2026-05-21",
    ]

    resultados = []

    logging.info("")
    logging.info("=" * 90)
    logging.info("[REPROCESSAMENTO][MANUAL] iniciado")
    logging.info("=" * 90)

    for data_jogo in datas_jogo:

        logging.info("")
        logging.info("=" * 90)
        logging.info(
            f"[REPROCESSAMENTO][MANUAL] "
            f"DATA={data_jogo}"
        )
        logging.info("=" * 90)

        # ===========================================
        # EVENTS
        # ===========================================

        df_events = extrair_eventos_por_datas_jogo(
            [data_jogo]
        )

        if df_events.empty:

            logging.warning(
                f"[REPROCESSAMENTO][MANUAL] "
                f"sem eventos | data={data_jogo}"
            )

            continue

        # ===========================================
        # TICKETS
        # ===========================================

        df_tickets = montar_df_tickets(
            df_events=df_events,
            start_datetime="01/01/2020 00:00",
            end_datetime="31/12/2026 23:59"
        )

        if df_tickets.empty:

            logging.warning(
                f"[REPROCESSAMENTO][MANUAL] "
                f"sem tickets | data={data_jogo}"
            )

            continue

        # ===========================================
        # CLIENTS
        # ===========================================

        df_clients = extrair_clients_por_tickets(
            df_tickets
        )

        # ===========================================
        # TRANSFORM
        # ===========================================

        df_events_tr = transformar_events(
            df_events
        )

        df_tickets_tr = transformar_tickets(
            df_tickets
        )

        if (
            df_clients is not None
            and not df_clients.empty
        ):

            df_clients_tr = transformar_clients(
                df_clients,
                data_insercao=data_jogo
            )

        else:

            df_clients_tr = None

            logging.info(
                "[REPROCESSAMENTO][MANUAL] "
                "clients vazio"
            )

        # ===========================================
        # LOAD
        # ===========================================

        if (
            df_events_tr is not None
            and not df_events_tr.empty
        ):
            load_events(df_events_tr)

        if (
            df_clients_tr is not None
            and not df_clients_tr.empty
        ):
            load_clients(df_clients_tr)

        load_tickets_stg(df_tickets_tr)

        load_dim_partida()

        load_ft_compraingresso(df_tickets_tr)

        load_cogny_ticket_integration(df_tickets_tr)

        logging.info(
            f"[REPROCESSAMENTO][MANUAL] "
            f"fim | linhas={len(df_tickets_tr)}"
        )

        resultados.append(df_tickets_tr)

    if not resultados:
        return pd.DataFrame()

    return pd.concat(
        resultados,
        ignore_index=True
    )


# ===========================================
# REPROCESSAMENTO TASK SCHEDULER
# ===========================================

def executar_reprocessamento_scheduler():

    logging.info("")
    logging.info("=" * 90)
    logging.info("[REPROCESSAMENTO][SCHEDULER] iniciado")
    logging.info("=" * 90)

    # ===========================================
    # EVENTS FUTUROS
    # ===========================================

    df_events_future = extrair_eventos_30_dias()

    if (
        df_events_future is not None
        and not df_events_future.empty
    ):

        logging.info(
            "[REPROCESSAMENTO][SCHEDULER] "
            f"events futuros={len(df_events_future)}"
        )

        df_events_future_tr = transformar_events(
            df_events_future
        )

        load_events(df_events_future_tr)

    # ===========================================
    # EVENTO ATIVO
    # ===========================================

    sk_partida = buscar_evento_futuro()

    if sk_partida is None:

        logging.warning(
            "[REPROCESSAMENTO][SCHEDULER] "
            "sem evento ativo"
        )

        return pd.DataFrame()

    logging.info(
        "[REPROCESSAMENTO][SCHEDULER] "
        f"evento ativo={sk_partida}"
    )

    # ===========================================
    # RANGE
    # ===========================================

    start_datetime = "01/01/2000 00:00"

    ontem = (
        datetime.now(TIMEZONE) - timedelta(days=1)
    )

    end_datetime = ontem.strftime(
        "%d/%m/%Y 23:59"
    )

    # ===========================================
    # EVENTS
    # ===========================================

    df_events = extrair_eventos_por_periodo(
        start_date="2000-01-01",
        end_date="2100-01-01"
    )

    if df_events.empty:

        logging.warning(
            "[REPROCESSAMENTO][SCHEDULER] "
            "sem eventos"
        )

        return pd.DataFrame()

    # ===========================================
    # EVENTO BASE
    # ===========================================

    df_events = definir_evento_jogo_base(
        df_events
    )

    df_events["event_id"] = (
        df_events["event_id"]
        .astype(str)
    )

    # ===========================================
    # EVENTOS RELACIONADOS
    # ===========================================

    df_events = df_events[
        df_events["event_id_jogo_base"] == str(sk_partida)
    ].copy()

    logging.info(
        "[REPROCESSAMENTO][SCHEDULER] "
        f"eventos relacionados={len(df_events)}"
    )

    # ===========================================
    # TICKETS
    # ===========================================

    df_extract = montar_df_tickets(
        df_events=df_events,
        start_datetime=start_datetime,
        end_datetime=end_datetime
    )

    if df_extract.empty:

        logging.warning(
            "[REPROCESSAMENTO][SCHEDULER] "
            "extract vazio"
        )

        return pd.DataFrame()

    # ===========================================
    # CLIENTS
    # ===========================================

    df_clients = extrair_clients_por_tickets(
        df_extract
    )

    # ===========================================
    # TRANSFORM
    # ===========================================

    df_tickets_tr = transformar_tickets(
        df_extract
    )

    # ===========================================
    # CLIENTS TRANSFORM
    # ===========================================

    if (
        df_clients is not None
        and not df_clients.empty
    ):

        df_clients_tr = transformar_clients(
            df_clients,
            data_insercao=ontem.strftime("%Y-%m-%d")
        )

    else:

        df_clients_tr = None

    # ===========================================
    # LOAD
    # ===========================================

    if (
        df_clients_tr is not None
        and not df_clients_tr.empty
    ):
        load_clients(df_clients_tr)

    load_tickets_stg(df_tickets_tr)

    load_dim_partida()

    load_ft_compraingresso(df_tickets_tr)

    load_cogny_ticket_integration(df_tickets_tr)

    logging.info(
        "[REPROCESSAMENTO][SCHEDULER] "
        f"fim | linhas={len(df_tickets_tr)}"
    )

    return df_tickets_tr


# ===========================================
# REALTIME
# ===========================================

def buscar_evento_futuro():

    conn = connect_dw_prod()

    with conn.connect() as sql:

        result = sql.execute(text("""
            select sk_partida
            from dw_prd_flamengo.dm_mkt.dim_partida
            where dthr_partida >= current_timestamp()
            order by dthr_partida
            limit 1
        """)).fetchone()

    return result[0] if result else None


def buscar_eventos_realtime():

    conn = connect_dw_prod()

    with conn.connect() as sql:

        result = sql.execute(text("""

            with jogo_futuro as (

                select
                    partida,
                    dthr_partida::date as dt_partida
                from dw_prd_flamengo.dm_mkt.dim_partida
                where dthr_partida >= current_timestamp()
                order by dthr_partida
                limit 1

            )

            select
                fe.cod_evento
            from dw_prd_flamengo.dm_mkt.fcard_eventos fe
            cross join jogo_futuro jf
            where upper(fe.partida) like '%' || (
                upper(split_part(jf.partida, ' X ', 2))
            ) || '%'
            and fe.dt_evento::date = jf.dt_partida
            order by fe.cod_evento

        """)).fetchall()

    eventos = [str(x[0]) for x in result]

    logging.info(
        f"[REALTIME] eventos encontrados={eventos}"
    )

    return eventos


def deletar_range_pagamento(start_datetime):

    conn = connect_dw_prod()

    with conn.connect() as sql:

        sql.execute(text("""
            DELETE FROM DW_PRD_FLAMENGO.DM_MKT.FT_COMPRAINGRESSO_FCARD_REALTIME_TESTE
            WHERE data_pagamento >= :start
        """), {
            "start": start_datetime
        })

        sql.commit()

    logging.info(
        f"[DELETE] aplicado | start={start_datetime}"
    )


def executar_real_time():

    intervalo_segundos = 300

    agora = datetime.now(TIMEZONE)

    hoje = agora.date()

    ontem = hoje - timedelta(days=1)

    logging.info("")
    logging.info("=" * 90)
    logging.info("[REALTIME] iniciado")
    logging.info("=" * 90)

    # ==========================================
    # EVENTOS
    # ==========================================

    eventos_ids = buscar_eventos_realtime()

    if not eventos_ids:

        logging.warning(
            "[REALTIME] sem eventos"
        )

        return

    # ==========================================
    # FULL HISTÓRICO
    # ==========================================

    logging.info("")
    logging.info("=" * 90)
    logging.info("[FULL HISTÓRICO] início")
    logging.info("=" * 90)

    start_datetime = datetime(2000, 1, 1)

    end_datetime = datetime(
        ontem.year,
        ontem.month,
        ontem.day,
        23,
        59,
        59
    )

    df_historico = extract_real_time(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        eventos_ids=eventos_ids
    )

    if not df_historico.empty:

        df_historico = transformar_tickets(
            df_historico
        )

        deletar_range_pagamento(
            start_datetime=start_datetime
        )

        load_realtime(df_historico)

        logging.info(
            f"[FULL HISTÓRICO] linhas={len(df_historico)}"
        )

    else:

        logging.warning(
            "[FULL HISTÓRICO] vazio"
        )

    # ==========================================
    # LOOP REALTIME
    # ==========================================

    logging.info("")
    logging.info("=" * 90)
    logging.info("[LOOP REALTIME] iniciado")
    logging.info("=" * 90)

    execucao = 1

    while True:

        agora = datetime.now(TIMEZONE)

        # ==========================================
        # ENCERRA 23:55
        # ==========================================

        limite_encerramento = datetime(
            agora.year,
            agora.month,
            agora.day,
            23,
            55,
            0
        )

        if agora.replace(tzinfo=None) >= limite_encerramento:

            logging.info(
                "[REALTIME] encerrado 23:55"
            )

            break

        logging.info("")
        logging.info("=" * 90)
        logging.info(
            f"[EXEC {execucao}] REALTIME"
        )
        logging.info("=" * 90)

        # ==========================================
        # RANGE
        # ==========================================

        start_datetime = datetime(
            hoje.year,
            hoje.month,
            hoje.day,
            0,
            0,
            0
        )

        end_datetime = agora.replace(
            tzinfo=None
        )

        # ==========================================
        # EXTRACT
        # ==========================================

        df_realtime = extract_real_time(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            eventos_ids=eventos_ids
        )

        if df_realtime.empty:

            logging.info(
                "[REALTIME] extract vazio"
            )

            time.sleep(intervalo_segundos)

            execucao += 1

            continue

        # ==========================================
        # TRANSFORM
        # ==========================================

        df_realtime = transformar_tickets(
            df_realtime
        )

        if df_realtime.empty:

            logging.info(
                "[REALTIME] transform vazio"
            )

            time.sleep(intervalo_segundos)

            execucao += 1

            continue

        # ==========================================
        # DELETE
        # ==========================================

        deletar_range_pagamento(
            start_datetime=start_datetime
        )

        # ==========================================
        # LOAD
        # ==========================================

        load_realtime(df_realtime)

        logging.info(
            f"[EXEC {execucao}] linhas={len(df_realtime)}"
        )

        execucao += 1

        time.sleep(intervalo_segundos)