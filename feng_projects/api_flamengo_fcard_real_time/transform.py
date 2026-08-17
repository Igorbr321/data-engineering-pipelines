import logging
import re

import pandas as pd
import numpy as np
from unidecode import unidecode


def transformar_events(df_events):
    if df_events.empty:
        logging.warning("[TRANSFORM][EVENTS] nenhum evento recebido")
        return df_events

    df = df_events.copy()

    # --- juntar datas ---
    df["data_inicio_vendas"] = pd.to_datetime(
        df["sales_start_date"].astype(str) + " " + df["sales_start_time"].astype(str),
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )

    df["data_inicio_vendas_publico"] = pd.to_datetime(
        df["public_sale_start_date"].astype(str) + " " + df["public_sale_start_time"].astype(str),
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )

    df["data_final_vendas_publico"] = pd.to_datetime(
        df["sales_end"],
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )

    # --- estrutura final ---
    df = pd.DataFrame({
        "COD_EVENTO": df["event_id"].astype(str),
        "DT_EVENTO": df["event_date_iso"],
        "HR_EVENTO": df["event_time"],
        "PARTIDA": df["match"].apply(lambda x: unidecode(str(x)).upper()),
        "ESTADIO": df["stadium"].apply(lambda x: unidecode(str(x)).upper()),
        "CAMPEONATO": df["championship"].apply(lambda x: unidecode(str(x)).upper()),
        "TIPO_EVENTO": df["tipo_evento"],
        "COD_EVENTO_BASE": df["event_id_jogo_base"].astype(str),
        "PARTIDA_BASE": df["partida_base"].apply(lambda x: unidecode(str(x)).upper()),

        # NOVAS COLUNAS
        "DATA_INICIO_VENDAS": df["data_inicio_vendas"],
        "DATA_INICIO_VENDAS_PUBLICO": df["data_inicio_vendas_publico"],
        "DATA_FINAL_VENDAS_PUBLICO": df["data_final_vendas_publico"],
    })

    logging.info(f"[TRANSFORM][EVENTS] total={len(df)}")

    return df


def transformar_clients(df_clients, data_insercao=None):
    if df_clients.empty:
        logging.warning("[TRANSFORM][CLIENTS] nenhum cliente recebido")
        return df_clients

    qtd_entrada = len(df_clients)

    df = df_clients.copy()
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "document": "cpf",
        "city": "cidade",
        "address": "endereco",
        "state": "estado",
        "district": "bairro",
    })

    df = df.drop_duplicates(subset=["cpf"], keep="last")

    df["nome"] = (
        df["first_name"].fillna("").astype(str) + " " + df["last_name"].fillna("").astype(str)
    ).str.strip().str.upper()

    df["email"] = df["email"].fillna("").astype(str).str.upper()
    df["endereco"] = df["endereco"].fillna("NAO_INFORMADO").astype(str).str.upper()
    df["telefone"] = "NAO_INFORMADO"

    df["cpf"] = (
        df["cpf"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
        .str[:11]
    )

    qtd_antes_cpf = len(df)
    df = df[df["cpf"].notna()]
    df = df[df["cpf"] != ""]

    df["nome"] = df["nome"].str.replace(r"[^A-Za-zÀ-ÖØ-öø-ÿ\s]", "", regex=True)

    df["cep"] = (
        df["cep"]
        .fillna("NAO_INFORMADO")
        .astype(str)
        .str.replace("-", "", regex=False)
    )

    for col in ["endereco", "estado", "cidade", "bairro"]:
        df[col] = (
            df[col]
            .fillna("NAO_INFORMADO")
            .astype(str)
            .str.upper()
            .str.replace(r"[^A-Za-zÀ-ÖØ-öø-ÿ\s]", "", regex=True)
        )

    df["data_insercao"] = data_insercao or pd.Timestamp.now().strftime("%Y-%m-%d")
    df["fonte"] = "FUTEBOLCARD"

    df = df[
        [
            "email",
            "cpf",
            "endereco",
            "nome",
            "telefone",
            "cidade",
            "bairro",
            "estado",
            "cep",
            "data_insercao",
            "fonte",
        ]
    ]

    qtd_antes_privacidade = len(df)

    df = df[df["email"] != "EXCLUIDO@EXCLUIDO.COM"]
    df = df[df["nome"] != "PRIVACIDADE EXCLUIDO"]

    df = df.sort_values("data_insercao")
    df = df.drop_duplicates(subset=["cpf"], keep="last")

    logging.info(
        f"[TRANSFORM][CLIENTS] entrada={qtd_entrada} | final={len(df)} "
        f"| removidos_cpf={qtd_antes_cpf - len(df)} "
        f"| removidos_privacidade={qtd_antes_privacidade - len(df)}"
    )

    return df


def transformar_tickets(df_tickets):

    if df_tickets.empty:

        logging.warning(
            "[TRANSFORM][TICKETS] nenhum ticket recebido"
        )

        return df_tickets

    qtd_entrada = len(df_tickets)

    # ===========================================
    # COPY
    # ===========================================

    df = df_tickets.copy()

    df.columns = [
        unidecode(col.lower().strip())
        for col in df.columns
    ]

    # ===========================================
    # CORTESIA
    # ===========================================

    df.loc[
        df["sale_from"] == "VENDA PROIBIDA FLAMENGO",
        ["document", "name"]
    ] = [
        "-1",
        "CORTESIA",
    ]

    # ===========================================
    # MEMBER UNIQUE ID
    # ===========================================

    if "member_unique_id" not in df.columns:
        df["member_unique_id"] = None

    # ===========================================
    # COLUNAS
    # ===========================================

    colunas = [
        "event",
        "name",
        "document",
        "amount",
        "payment_method",
        "payment_date",
        "order_status",
        "used",
        "ticket_hash",
        "gate",
        "sector",
        "row",
        "seat",
        "order_id",
        "sale_from",
        "subsector",
        "ticket_id",
        "used_time",
        "member_fc_id",
        "client_id",
        "member_unique_id",
        "ticket_name",
        "ticket_document",
        "ipe_comprou_ano_vigente",
        "discount",
        "convenience_fee",
        "event_id_original",
        "event_id_jogo_base",
        "tipo_evento",
        "event_date",
        "event_date_iso",
        "event_time",
        "match",
        "partida_base",
        "championship",
        "stadium",
    ]

    for col in colunas:

        if col not in df.columns:
            df[col] = None

    df = df[colunas].copy()

    # ===========================================
    # RENAME
    # ===========================================

    df = df.rename(columns={
        "event": "cod_evento",
        "amount": "valor",
        "used": "usado",
        "ticket_hash": "ingresso",
        "order_status": "status_ingresso",
        "gate": "portao_acesso",
        "sector": "setor",
        "payment_date": "data_pagamento",
        "payment_method": "forma_pagamento",
        "row": "fileira",
        "seat": "assento",
        "discount": "desconto",
        "convenience_fee": "taxa_conveniencia",
    })

    # ===========================================
    # EVENTO ORIGINAL
    # ===========================================

    df["cod_evento"] = df["event_id_original"].where(
        df["event_id_original"].notna(),
        df["cod_evento"]
    )

    # ===========================================
    # STRINGS
    # ===========================================

    df["name"] = (
        df["name"]
        .fillna("")
        .astype(str)
        .str.upper()
    )

    df["valor"] = (
        df["valor"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    # ===========================================
    # DATAS
    # ===========================================

    df["data_pagamento"] = pd.to_datetime(
        df["data_pagamento"],
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )

    df["used_time"] = pd.to_datetime(
        df["used_time"],
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )

    df["used_time"] = df["used_time"].apply(
        lambda x:
            x.strftime("%Y-%m-%d %H:%M:%S")
            if pd.notnull(x)
            else None
    )

    # ===========================================
    # BOOLEAN
    # ===========================================

    df["usado"] = df["usado"].apply(
        lambda x:
            True
            if str(x).lower() == "true"
            else False
    )

    # ===========================================
    # STATUS
    # ===========================================

    qtd_antes_status = len(df)

    df["status_ingresso"] = (
        df["status_ingresso"]
        .astype(str)
        .str.upper()
        .map(lambda x: "PA" if x == "PAGO" else "CA")
    )

    df = df[
        df["status_ingresso"] == "PA"
    ].copy()

    # ===========================================
    # NORMALIZAÇÃO
    # ===========================================

    for col in [
        "portao_acesso",
        "setor",
        "fileira",
        "assento",
    ]:

        df[col] = df[col].apply(
            lambda x: unidecode(str(x))
        )

    # ===========================================
    # NOME
    # ===========================================

    df["nome"] = df["name"].where(
        df["name"].notna() &
        (df["name"].str.strip() != ""),
        df["ticket_name"]
    )

    df["nome"] = (
        df["nome"]
        .astype(str)
        .str.strip()
    )

    # ===========================================
    # CPF
    # ===========================================

    df["document"] = df["document"].replace(
        ["None", "nan", "NaN", ""],
        np.nan
    )

    df["document"] = df["document"].apply(
        lambda x:
            str(x).strip()
            if pd.notna(x)
            else None
    )

    df["cpf"] = df["document"]

    # ===========================================
    # DOCUMENTO PORTADOR
    # ===========================================

    df["documento_portador"] = df.get(
        "ticket_document",
        None
    )

    df["documento_portador"] = (
        df["documento_portador"]
        .replace(
            ["None", "nan", "NaN", ""],
            np.nan
        )
    )

    df["documento_portador"] = (
        df["documento_portador"]
        .apply(
            lambda x:
                str(x).strip()
                if pd.notna(x)
                else None
        )
    )

    # ===========================================
    # CORTESIA
    # ===========================================

    cond_cortesia = (
        df["forma_pagamento"]
        .astype(str)
        .str.strip()
        .str.upper()
        .isin([
            "PEDIDO DE CORTESIA",
            "CARGA",
        ])
    )

    qtd_cortesia = int(
        cond_cortesia.sum()
    )

    df.loc[
        cond_cortesia,
        "documento_portador"
    ] = "-1"

    # ===========================================
    # FLAG CPF PORTADOR
    # ===========================================

    df["flag_cpf_portador"] = (
        df["documento_portador"]
        .apply(
            lambda x:
                True
                if (
                    str(x).isdigit()
                    and len(str(x)) == 11
                )
                else False
        )
    )

    # ===========================================
    # CPF PADRÃO
    # ===========================================

    df["cpf"] = df["cpf"].where(
        df["cpf"].notna() &
        (df["cpf"] != ""),
        "-1"
    )

    # ===========================================
    # TAXA
    # ===========================================

    df["taxa_conveniencia"] = (
        df["taxa_conveniencia"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    # ===========================================
    # DESCONTO
    # ===========================================

    df["desconto"] = (
        df["desconto"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["desconto"] = (
        df["desconto"]
        .str.replace(
            r"[^A-Za-zÀ-ÖØ-öø-ÿ\s]",
            "",
            regex=True
        )
    )

    df["desconto"] = df["desconto"].apply(
        lambda x:
            x[:200]
            if x is not None
            else ""
    )

    df.loc[
        df["desconto"].isna() |
        (df["desconto"] == ""),
        "desconto"
    ] = "NÃO INFORMADO"

    # ===========================================
    # PDV
    # ===========================================

    df.loc[
        (
            df["sale_from"] == "PDV FLAMENGO"
        ) &
        (
            df["cpf"].isna() |
            (df["cpf"] == "")
        ),
        ["cpf", "nome"],
    ] = [
        "-1",
        "PDV",
    ]

    # ===========================================
    # TICKET NAME
    # ===========================================

    df["ticket_name"] = (
        df["ticket_name"]
        .fillna("")
        .astype(str)
        .str.replace(
            "Documento: ",
            "",
            regex=False
        )
        .str.strip()
    )

    # ===========================================
    # CPF FINAL
    # ===========================================

    df["cpf"] = (
        df["cpf"]
        .astype(str)
        .str.replace(
            r"\D",
            "",
            regex=True
        )
    )

    df["cpf"] = df["cpf"].where(
        df["cpf"] != "",
        "-1"
    )

    df["cpf"] = df["cpf"].str[:11]

    # ===========================================
    # NOME FINAL
    # ===========================================

    df["nome"] = (
        df["nome"]
        .astype(str)
        .str.replace(
            r"[^A-Za-zÀ-ÖØ-öø-ÿ\s]",
            "",
            regex=True
        )
    )

    # ===========================================
    # OBJECTS
    # ===========================================

    for col in df.columns:

        if col == "used_time":
            continue

        if df[col].dtype == "object":

            df[col] = (
                df[col]
                .astype(str)
                .replace(
                    ["nan", "None"],
                    ""
                )
                .str.upper()
            )

    # ===========================================
    # SETOR
    # ===========================================

    df["setor"] = (
        df["setor"]
        .astype(str)
        .str.replace(
            r"[^A-Za-zÀ-ÖØ-öø-ÿ\s]",
            "",
            regex=True
        )
    )

    df["setor"] = (
        df["setor"]
        .replace("", None)
        .fillna("NAO_INFORMADO")
    )

    df["setor"] = df["setor"].apply(
        lambda x: " ".join(str(x).split())
    )

    # ===========================================
    # LIMITES
    # ===========================================

    df["cpf"] = df["cpf"].apply(
        lambda x:
            x[:11]
            if x is not None
            else ""
    )

    df["nome"] = df["nome"].apply(
        lambda x:
            x[:100]
            if x is not None
            else ""
    )

    df.loc[
        df["cpf"] == "1",
        "cpf"
    ] = "-1"

    # ===========================================
    # NUMÉRICOS
    # ===========================================

    colunas_numericas = [
        "client_id",
        "member_fc_id",
        "member_unique_id",
    ]

    for col in colunas_numericas:

        if col not in df.columns:
            continue

        df[col] = (
            df[col]
            .replace(
                ["", "NONE", "NAN"],
                np.nan
            )
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # ===========================================
    # FINAL
    # ===========================================

    df = df[
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
            "tipo_evento",
            "event_id_jogo_base",
            "partida_base",
        ]
    ]

    df = df.replace({
        np.nan: None
    })

    logging.info(
        f"[TRANSFORM][TICKETS] entrada={qtd_entrada} | "
        f"final={len(df)} "
        f"| removidos_status={qtd_antes_status - len(df)} "
        f"| cortesia={qtd_cortesia} "
        f"| cpf_portador={df['flag_cpf_portador'].value_counts(dropna=False).to_dict()} "
        f"| resumo={df['tipo_evento'].value_counts(dropna=False).to_dict()}"
    )

    return df


def transform_all(resultado_extract, data_insercao=None):
    resultado = {
        "events": transformar_events(resultado_extract["events"]),
        "tickets": transformar_tickets(resultado_extract["tickets"]),
        "clients": transformar_clients(resultado_extract["clients"], data_insercao),
    }

    resultado["tickets"].to_csv(
        "tickets_transformados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    logging.info(
        "[TRANSFORM][ALL] csv=tickets_transformados.csv "
        f"| events={len(resultado['events'])} "
        f"| tickets={len(resultado['tickets'])} "
        f"| clients={len(resultado['clients'])}"
    )

    return resultado