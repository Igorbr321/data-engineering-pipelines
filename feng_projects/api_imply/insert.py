import logging
import pandas as pd

from utils import connect_dw_lake_vasco
from sqlalchemy import text
from snowflake.connector.pandas_tools import pd_writer

from query import SQL_UPSERT_DIM_PARTIDA


def inserir_lake_fla(df: pd.DataFrame, date_start: str, date_end: str) -> None:
    logging.info("🟡 [VASCO] - Inserindo os dados na tabela teste DW_STG_MKT.GOLD.FT_COMPRAINGRESSO_IMPLY.")

    conn = connect_dw_lake_vasco()

    target_table = "DW_STG_MKT.GOLD.FT_COMPRAINGRESSO_IMPLY"
    temp_table = "stg_ft_compraingresso_imply_temp"  # TEMP table (sessão)

    with conn.connect() as sql:
        # 1) cria tabela temporária igual a tabela alvo
        logging.info("🟡 [VASCO] - Criando staging temporária")
        sql.execute(text(f"CREATE OR REPLACE TEMP TABLE {temp_table} LIKE {target_table};"))

        # 2) carrega df na staging temporária
        if df.empty:
            logging.info("🟡 [VASCO] - DataFrame vazio. Nada para inserir.")
            return

        logging.info(f"🟡 [VASCO] - Carregando staging temporária: {len(df)} linhas")
        df.to_sql(
            name=temp_table,
            con=sql,
            if_exists="append",
            index=False,
            method=pd_writer,
        )

        # 3) delete por CODIGO usando a staging temporária
        logging.info("🟡 [VASCO] - Deletando na tabela final por CODIGO (via staging temp)")
        sql.execute(
            text(f"""
                DELETE FROM {target_table} t
                USING {temp_table} s
                WHERE t.CODIGO = s.CODIGO;
            """)
        )

        # 4) insere na tabela final a partir da staging temporária
        logging.info("🟡 [VASCO] - Inserindo na tabela final a partir da staging temp (STATUS='PA')")
        sql.execute(
            text(f"""
                INSERT INTO {target_table}
                SELECT * FROM {temp_table}
                WHERE STATUS = 'PA';
            """)
        )

        # 5) atualiza DIM_PARTIDA no GOLD (pós-carga)
        logging.info("🟡 [VASCO] - Atualizando DW_STG_MKT.GOLD.DIM_PARTIDA (UPSERT incremental)")
        sql.execute(SQL_UPSERT_DIM_PARTIDA)

        sql.commit()

    logging.info(
        f"🟡 [VASCO] - Execução concluída: {len(df)} registros carregados (temp) + delete + insert + update DIM_PARTIDA."
    )
