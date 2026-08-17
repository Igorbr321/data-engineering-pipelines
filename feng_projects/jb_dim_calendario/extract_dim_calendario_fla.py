import logging
import pandas as pd

from utils import connect_dw_lake_fla
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def extract_dim_calendario_fla() -> pd.DataFrame:
    try:
        conn = connect_dw_lake_fla()

        with conn.begin() as sql:
            query = text("""
                SELECT *
                FROM dw_prd_flamengo.dm_mkt.dim_calendario
            """)

            result = sql.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            df.columns = df.columns.str.upper()

            logging.info(f"✅ Extração concluída com sucesso: {len(df)} registros.")
            return df

    except SQLAlchemyError as e:
        logging.error(f"❌ Erro ao extrair dados do DW: {e}")
        return pd.DataFrame()