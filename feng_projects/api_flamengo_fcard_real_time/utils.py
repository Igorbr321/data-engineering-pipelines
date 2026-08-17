import os 
import time
import logging
import pandas as pd 

from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, DBAPIError
from snowflake.connector.errors import DatabaseError as SnowflakeDatabaseError

load_dotenv()


# =============================
# Conexão Lake FLAMENGO
# =============================

def connect_dw_fla(database, retries=10, delay=60):
    db_url = (
        f"snowflake://{os.getenv('USER_DW_FLA')}:"
        f"{os.getenv('PASSWORD_DW_FLA')}@"
        f"{os.getenv('HOST_DW_FLA')}/"
        f"{database}?warehouse={os.getenv('WAREHOUSE_DW_FLA')}"
    )

    for attempt in range(1, retries + 1):
        try:
            conn = create_engine(db_url)

            with conn.connect() as sql:
                sql.execute(text("select 1"))
                logging.info(f"Conectado ao DW | database={database}")

            return conn

        except (OperationalError, DBAPIError, SnowflakeDatabaseError) as e:
            logging.warning(f"Tentativa {attempt} falhou: {e}")

            if attempt < retries:
                time.sleep(delay)
            else:
                raise


# =============================
# Conexão Lake STG e PROD
# =============================
def connect_dw_stg():
    return connect_dw_fla("STG_PRD_FLAMENGO")

def connect_dw_prod():
    return connect_dw_fla("DW_PRD_FLAMENGO")


# =============================
# Inicialização de logging
# =============================

def init_logging():
    import warnings
    from sqlalchemy.exc import SAWarning

    logging.basicConfig(
        filename="app.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )

    # ignora logs de INFO e DEBUG do Snowflake
    logging.getLogger("snowflake.connector").setLevel(logging.WARNING)
    warnings.filterwarnings(
        "ignore",
        category=SAWarning,
        message="The GenericFunction 'flatten' is already registered and is going to be overridden.",
    )


# =============================
# Conexão para armazenar log
# =============================

def save_logs(program, table, execution_time, error):
    logs = ""

    # Ler o conteúdo do arquivo de log
    with open("app.log", "r", encoding="utf-8") as log_file:
        logs = log_file.read()

    df = pd.DataFrame(
        [
            {
                "programa": program,
                "tabela": table,
                "duracao": execution_time,
                "logs": logs,
                "erro": error,
                "data_processamento": datetime.now(),
            }
        ]
    )

    conn = connect_dw_lake_fla()
    with conn.connect() as sql:
        df.to_sql(
            "logs_processos",
            sql,
            schema="bi_ods",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1,
        )
        sql.commit()
        logging.info(f"Log de execução salvo no banco de dados.")


# =============================
# Tempo de Execução
# =============================

def execution_time(start_time):
    import time

    execution_time = time.time() - start_time
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)

    return round(minutes + (seconds / 100), 2)