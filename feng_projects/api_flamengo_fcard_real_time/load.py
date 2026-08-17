import logging

import pandas as pd
from sqlalchemy import text

from utils import connect_dw_stg, connect_dw_prod


def _get_event_ids(df):
    return (
        df["cod_evento"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .tolist()
    )


def _sql_in_values(values):
    return ", ".join(
        f"'{str(v).replace(chr(39), chr(39) + chr(39))}'"
        for v in values
    )


def load_events(df_events):
    if df_events.empty:
        logging.warning("[LOAD][EVENTS] nenhum evento para carregar")
        return

    df = df_events[
        [
            "COD_EVENTO",
            "DT_EVENTO",
            "HR_EVENTO",
            "PARTIDA",
            "ESTADIO",
            "CAMPEONATO",
            "DATA_INICIO_VENDAS",
            "DATA_INICIO_VENDAS_PUBLICO",
            "DATA_FINAL_VENDAS_PUBLICO",
        ]
    ].copy()

    eventos = df["COD_EVENTO"].dropna().astype(str).drop_duplicates().tolist()

    conn = connect_dw_prod()

    with conn.connect() as sql:
        for cod_evento in eventos:
            sql.execute(
                text("""
                    delete from dm_mkt.fcard_eventos
                    where cod_evento = :cod_evento
                """),
                {"cod_evento": cod_evento}
            )

        sql.commit()

        df.to_sql(
            "fcard_eventos",
            sql,
            schema="dm_mkt",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )

        sql.commit()

    logging.info(f"[LOAD][EVENTS] carregados={len(df)} | eventos={eventos}")


def load_clients(df_clients):
    if df_clients.empty:
        logging.warning("[LOAD][CLIENTS] nenhum cliente para carregar")
        return

    df = df_clients[
        [
            "cpf",
            "nome",
            "email",
            "estado",
            "cidade",
            "bairro",
            "endereco",
            "cep",
            "telefone",
            "fonte",
            "data_insercao",
        ]
    ].copy()

    conn = connect_dw_stg()

    with conn.connect() as sql:
        sql.execute(text("""
            create temporary table stg_mkt.temp_stg_sat_pessoa_fcard (
                cpf varchar(20),
                nome varchar(120),
                email varchar(150),
                estado varchar(150),
                cidade varchar(100),
                bairro varchar(100),
                endereco varchar(150),
                cep varchar(150),
                telefone varchar(50),
                fonte varchar(150),
                data_insercao date
            )
        """))

        sql.commit()

        df.to_sql(
            "temp_stg_sat_pessoa_fcard",
            sql,
            schema="stg_mkt",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=10000,
        )

        sql.commit()

        sql.execute(text("""
            merge into stg_mkt.stg_sat_pessoa_fcard as a
            using stg_mkt.temp_stg_sat_pessoa_fcard as b
                on a.cpf = b.cpf

            when matched and (
                a.nome != b.nome or
                a.email != b.email or
                a.estado != b.estado or
                a.cidade != b.cidade or
                a.bairro != b.bairro or
                a.endereco != b.endereco or
                a.cep != b.cep or
                a.fonte != b.fonte
            ) then update set
                a.nome = b.nome,
                a.email = b.email,
                a.estado = b.estado,
                a.cidade = b.cidade,
                a.bairro = b.bairro,
                a.endereco = b.endereco,
                a.cep = b.cep,
                a.fonte = b.fonte

            when not matched then insert (
                cpf,
                nome,
                email,
                estado,
                cidade,
                bairro,
                endereco,
                cep,
                telefone,
                fonte,
                data_insercao
            )
            values (
                b.cpf,
                b.nome,
                b.email,
                b.estado,
                b.cidade,
                b.bairro,
                b.endereco,
                b.cep,
                b.telefone,
                b.fonte,
                b.data_insercao
            )
        """))

        sql.commit()

    logging.info(f"[LOAD][CLIENTS] merge concluído | linhas={len(df)}")


def load_tickets_stg(df_tickets):
    if df_tickets.empty:
        logging.warning("[LOAD][TICKETS_STG] nenhum ticket para carregar")
        return

    df = df_tickets[
        [
            "cod_evento",
            "cpf",
            "nome",
            "ingresso",
            "status_ingresso",
            "valor",
            "data_pagamento",
            "forma_pagamento",
            "usado",
            "setor",
            "portao_acesso",
            "fileira",
            "assento",
            "order_id",
            "sale_from",
            "subsector",
            "ticket_id",
            "used_time",
            "member_fc_id",
            "client_id",
            "member_unique_id",
            "ipe_comprou_ano_vigente",
            "desconto",
            "taxa_conveniencia",
            "ticket_name",
            "documento_portador",
            "flag_cpf_portador",
        ]
    ].copy()

    df = df.where(pd.notna(df), None)

    eventos = _get_event_ids(df)

    conn = connect_dw_stg()

    with conn.connect() as sql:
        for cod_evento in eventos:
            sql.execute(
                text("""
                    delete from stg_mkt.stg_ft_compraingresso_fcard
                    where cod_evento = :cod_evento
                """),
                {"cod_evento": cod_evento}
            )

        sql.commit()

        df.to_sql(
            "stg_ft_compraingresso_fcard",
            sql,
            schema="stg_mkt",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=10000,
        )

        sql.commit()

    logging.info(f"[LOAD][TICKETS_STG] carregados={len(df)} | eventos={eventos}")


def load_dim_partida():
    conn = connect_dw_prod()

    with conn.connect() as sql:
        sql.execute(text("""
            insert into dw_prd_flamengo.dm_mkt.dim_partida
            select
                cod_evento as sk_partida,
                a.partida,
                a.campeonato || ' ' || year(a.dt_evento::date) as campeonato,
                (a.dt_evento || ' ' || a.hr_evento) as dthr_partida
            from dw_prd_flamengo.dm_mkt.fcard_eventos a
            left join dw_prd_flamengo.dm_mkt.dim_partida b
                on a.cod_evento = b.sk_partida
            where b.sk_partida is null
                and upper(a.partida) not like '%ESPACO%'
                and upper(a.partida) not like '%FLA+%'
                and upper(a.partida) not like '%ESTACIONAMENTO%'
        """))

        sql.commit()

    logging.info("[LOAD][DIM_PARTIDA] carga incremental concluída somente para jogos")


def load_ft_compraingresso(df_tickets):
    if df_tickets.empty:
        logging.warning("[LOAD][FT_COMPRAINGRESSO] nenhum ticket para carregar")
        return

    eventos = _get_event_ids(df_tickets)
    eventos_sql = _sql_in_values(eventos)

    conn = connect_dw_prod()

    with conn.connect() as sql:
        for cod_evento in eventos:
            sql.execute(
                text("""
                    delete from dw_prd_flamengo.dm_mkt.ft_compraingresso_fcard
                    where sk_partida = :cod_evento
                """),
                {"cod_evento": cod_evento}
            )

        sql.commit()

        sql.execute(text(f"""
            insert into dw_prd_flamengo.dm_mkt.ft_compraingresso_fcard
            select
                a.cod_evento as sk_partida,
                b.sk_pessoa,
                a.ingresso,
                a.cpf,
                a.valor,
                a.data_pagamento,
                a.forma_pagamento,
                a.usado,
                a.setor,
                a.portao_acesso,
                a.fileira,
                a.assento,
                a.desconto,
                a.taxa_conveniencia,
                ultc.sk_contrato,
                a.used_time as data_acesso,
                a.ticket_name as nome_portador,
                a.documento_portador,
                a.flag_cpf_portador
            from stg_prd_flamengo.stg_mkt.stg_ft_compraingresso_fcard a
            left join dw_prd_flamengo.dm_mkt.dim_pessoa b
                on a.cpf = b.cpf
            and b.load_end_date is null
            left join dw_prd_flamengo.dm_mkt.vw_ultimocontrato_st ultc
                on a.cpf = ultc.cpf
            where a.cod_evento in ({eventos_sql})
        """))

        sql.commit()

    logging.info(f"[LOAD][FT_COMPRAINGRESSO] eventos={eventos}")


def load_cogny_ticket_integration(df_tickets):
    if df_tickets.empty:
        logging.warning("[LOAD][COGNY] nenhum ticket para carregar")
        return

    eventos = _get_event_ids(df_tickets)
    eventos_sql = _sql_in_values(eventos)

    conn = connect_dw_prod()

    with conn.connect() as sql:
        for cod_evento in eventos:
            sql.execute(
                text("""
                    delete from dw_prd_flamengo.dm_mkt.cogny_ticket_integration
                    where event = :cod_evento
                """),
                {"cod_evento": cod_evento}
            )

        sql.commit()

        sql.execute(text(f"""
            insert into dw_prd_flamengo.dm_mkt.cogny_ticket_integration
            select
                fe.partida,
                fe.dt_evento as data_realizacao,
                fc.ingresso,
                fc.portao_acesso as tipo_acesso,
                fc.valor,
                fc.cpf,
                coalesce(dp.nome, dpf.nome, fc.nome),
                coalesce(dp.email, dpf.email),
                fc.setor,
                'NAO_INFORMADO' as descricao,
                'FCARD' as ticketeira,
                fc.usado as used,
                fc.fileira as "row",
                fc.assento as seat,
                fe.cod_evento as event,
                fc.order_id,
                fc.sale_from,
                fc.subsector,
                fc.ticket_id,
                fc.used_time,
                fc.member_fc_id,
                fc.client_id,
                'PAGO' as order_status,
                fc.data_pagamento as payment_date,
                fc.forma_pagamento as payment_method,
                case
                    when fc.member_unique_id in ('', 'null') then null
                    else fc.member_unique_id
                end as member_unique_id,
                fc.ipe_comprou_ano_vigente,
                fc.desconto,
                fc.taxa_conveniencia,
                fc.ticket_name,
                fc.documento_portador,
                fc.flag_cpf_portador
            from stg_prd_flamengo.stg_mkt.stg_ft_compraingresso_fcard fc
            inner join dw_prd_flamengo.dm_mkt.fcard_eventos fe
                on fc.cod_evento = fe.cod_evento
            left join dw_prd_flamengo.dm_mkt.dim_pessoa dp
                on fc.cpf = dp.cpf
                and dp.load_end_date is null
                and dp.email is not null
            left join stg_prd_flamengo.stg_mkt.stg_sat_pessoa_fcard dpf
                on fc.cpf = dpf.cpf
                and dpf.email is not null
            where fc.cod_evento in ({eventos_sql})
        """))

        sql.commit()

    logging.info(f"[LOAD][COGNY] eventos={eventos}")


def load_all(df_events, df_clients, df_tickets):
    logging.info("[LOAD] inicio")

    load_events(df_events)
    load_clients(df_clients)
    load_tickets_stg(df_tickets)
    load_dim_partida()
    load_ft_compraingresso(df_tickets)
    load_cogny_ticket_integration(df_tickets)

    logging.info("[LOAD] fim")


def load_realtime(df):

    colunas = [
        "cod_evento",
        "cpf",
        "nome",
        "ingresso",
        "status_ingresso",
        "valor",
        "data_pagamento",
        "forma_pagamento",
        "usado",
        "setor",
        "portao_acesso",
        "fileira",
        "assento",
        "order_id",
        "sale_from",
        "subsector",
        "ticket_id",
        "used_time",
        "member_fc_id",
        "client_id",
        "member_unique_id",
        "ipe_comprou_ano_vigente",
        "desconto",
        "taxa_conveniencia",
        "ticket_name",
        "documento_portador",
        "flag_cpf_portador"
    ]

    df = df.reindex(columns=colunas)

    conn = connect_dw_prod()

    df.to_sql(
        "ft_compraingresso_fcard_realtime",
        conn,
        schema="DM_MKT",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=10000,
    )

    logging.info(
        f"[LOAD] inserido | linhas={len(df)}"
    )