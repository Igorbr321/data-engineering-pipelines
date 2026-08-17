import pandas as pd
import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from utils import connect_dw_central


def extract_dim_cep_central() -> pd.DataFrame:
    logging.info(
        "🚀 Iniciando a extração dos dados da DIM_CEP."
    )

    try:
        conn = connect_dw_central()

        with conn.begin() as sql:
            query = text("""
                SELECT *
                FROM FENG_BI.BI_DIM.DIM_CEP
            """)

            result = sql.execute(query)

            df = pd.DataFrame(
                result.fetchall(),
                columns=result.keys()
            )

        logging.info(
            f"✅ Extração concluída com sucesso: {len(df)} registros."
        )

        return df

    except SQLAlchemyError as e:
        logging.error(f"❌ Erro ao extrair dados do DW: {e}")
        return pd.DataFrame()