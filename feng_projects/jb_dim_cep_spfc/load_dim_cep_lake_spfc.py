import pandas as pd
import logging

from sqlalchemy.exc import SQLAlchemyError
from utils import connect_dw_lake


def load_dim_cep_lake(df: pd.DataFrame):
    logging.info(
        "🚀 Inserindo os dados da DIM_CEP em DIM_CEP LAKE."
    )

    try:
        conn = connect_dw_lake()

        with conn.begin() as sql:

            df.to_sql(
                name="dim_cep",
                con=sql,
                schema="BRONZE",
                index=False,
                if_exists="append",
                method="multi",
            )

        logging.info(
            f"✅ Inserção concluída: {len(df)} registros inseridos."
        )

    except SQLAlchemyError as e:
        logging.error(f"❌ Erro ao inserir dados no LAKE: {e}")