import logging
import pandas as pd

from utils import connect_dw_lake_fla
from sqlalchemy import text
from snowflake.connector.pandas_tools import pd_writer


def inserir_master(df: pd.DataFrame) -> None:
    logging.info("🔵 [MASTER] Inserindo dados Master - DIM_PESSOA_ECOMMERCE")

    engine = connect_dw_lake_fla()

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE DM_ECOMMERCE.DIM_PESSOA_ECOMMERCE"))

        df.to_sql(
            name="dim_pessoa_ecommerce",
            con=conn,
            schema="DM_ECOMMERCE",
            index=False,
            if_exists="append",
            method=pd_writer,
        )

    logging.info(f"🔵 [MASTER] Inserção concluída: {len(df)} registros inseridos.")