import logging
import pandas as pd

from utils import connect_dw_spfc, connect_dw_vasco
from sqlalchemy import text
from snowflake.connector.pandas_tools import pd_writer

tag_spfc = "SPFC"

tag_vasco = "VASCO"

def inserir_lake_vasco(df: pd.DataFrame):
    logging.info('Inserindo os dados.')

    conn = connect_dw_vasco()

    with conn.connect() as sql:
        df.to_sql(
            name="dim_calendario",
            con=sql,
            schema="SILVER",
            index=False,
            if_exists="append",
            method=pd_writer
        )

    logging.info(f"{tag_vasco}: ✅ inserção concluída: {len(df)} registros inseridos.")



def inserir_lake_spfc(df: pd.DataFrame):
    logging.info('Inserindo os dados.')

    conn = connect_dw_spfc()

    with conn.connect() as sql:
        df.to_sql(
            name="dim_calendario",
            con=sql,
            schema="SILVER",
            index=False,
            if_exists="append",
            method=pd_writer
        )

    logging.info(f"{tag_spfc}: ✅ inserção concluída: {len(df)} registros inseridos.")