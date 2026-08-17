import os 
import time
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, DBAPIError
from snowflake.connector.errors import DatabaseError as SnowflakeDatabaseError

load_dotenv()

# =============================
# Conexão com Lake Flamengo
# =============================

def connect_dw_lake_fla(retries=10, delay=60):
    db_url = f"snowflake://{os.getenv('USER_DW_FLA')}:{os.getenv('PASSWORD_DW_FLA')}@{os.getenv('HOST_DW_FLA')}/{os.getenv('NAME_DW_FLA')}?warehouse={os.getenv('WAREHOUSE_DW_FLA')}"

    for attempt in range(1, retries + 1):
        try:
            conn = create_engine(db_url)
            with conn.connect() as sql:
                sql.execute(text("select 1"))
                logging.info("🟡 Conectado ao DW")
            return conn
        except (OperationalError, DBAPIError, SnowflakeDatabaseError) as e:
            logging.info(f"Tentativa {attempt} falhou: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise


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
# Tempo de Execução
# =============================

def execution_time(start_time):
    import time

    execution_time = time.time() - start_time
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)

    return round(minutes + (seconds / 100), 2)

