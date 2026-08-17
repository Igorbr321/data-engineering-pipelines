import logging
import pandas as pd

from utils import connect_dw_lake_fla
from sqlalchemy import text
from snowflake.connector.pandas_tools import pd_writer


def inserir_pedidos(df: pd.DataFrame) -> None:
    logging.info("🟢 [PEDIDOS] Inserindo dados de Pedidos - FT_PEDIDOS_ECOMMERCE")

    engine = connect_dw_lake_fla()

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE DM_ECOMMERCE.FT_PEDIDOS_ECOMMERCE"))

        df.to_sql(
            name="ft_pedidos_ecommerce",
            con=conn,
            schema="DM_ECOMMERCE",
            index=False,
            if_exists="append",
            method=pd_writer,
        )

    logging.info(f"🟢 [PEDIDOS] Inserção concluída: {len(df)} registros inseridos.")