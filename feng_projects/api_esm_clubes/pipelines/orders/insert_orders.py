import logging
import pandas as pd

from common.utils import connect_dw_lake_spfc
from sqlalchemy import text
from snowflake.connector.pandas_tools import pd_writer


def inserir_ordens_esm(
    df: pd.DataFrame,
    date_start: str,
    date_end: str
) -> None:
    logging.info(
        f"🟢 [ORDERS] - Deletando e inserindo período: {date_start} -> {date_end}"
    )

    conn = connect_dw_lake_spfc()

    with conn.connect() as sql:
        sql.execute(
            text("""
                DELETE FROM DW_STG_MKT.BRONZE.stg_dim_ordens_esm
                WHERE TRY_TO_TIMESTAMP_NTZ(SALE_DATE) >= TO_TIMESTAMP_NTZ(:date_start)
                AND TRY_TO_TIMESTAMP_NTZ(SALE_DATE) <  DATEADD(day, 1, TO_TIMESTAMP_NTZ(:date_end));
            """),
            {"date_start": date_start, "date_end": date_end},
        )


        if not df.empty:
            df.to_sql(
                "stg_dim_ordens_esm",
                con=sql,
                schema="BRONZE",
                if_exists="append",
                index=False,
                method=pd_writer,
                chunksize=10000,
            )

        sql.commit()
