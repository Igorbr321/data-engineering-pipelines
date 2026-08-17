import os 
import time
import logging
import warnings
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, DBAPIError
from snowflake.connector.errors import DatabaseError as SnowflakeDatabaseError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

load_dotenv()

# =============================
# Key Pair - Vasco
# =============================

def gen_private_key_vasco():
    passphrase = os.getenv("DB_PRIVATE_KEY_PASSPHRASE_VASCO")
    key_content = os.getenv("DB_PRIVATE_KEY_CONTENT_VASCO")

    # Reconstroi a chave privada, porque no .env tivemos que colocar quebras \n, para compartilhar de uma forma prática a private key.
    private_key_decoded = key_content.replace("\\n", "\n")

    private_key = serialization.load_pem_private_key(
        private_key_decoded.encode(),
        password=passphrase.encode(),
        backend=default_backend(),
    )

    # Snowflake exige formato DER PKCS8
    private_key_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return private_key_der

# =============================
# Conexão com Vasco
# =============================

def connect_dw_vasco(retries=10, delay=60):
    db_url = f"snowflake://{os.getenv('DB_USER_VASCO')}@{os.getenv('DB_HOST_VASCO')}/?warehouse={os.getenv('DB_WAREHOUSE_VASCO')}&database={os.getenv('DB_NAME_VASCO')}"

    for attempt in range(1, retries + 1):
        try:
            conn = create_engine(
                db_url, connect_args={"private_key": gen_private_key_vasco()}
            )

            with conn.connect() as sql:
                sql.execute(text("SELECT 1"))
                logging.info("Conectado ao DW com sucesso.")

            return conn

        except (OperationalError, DBAPIError, SnowflakeDatabaseError) as e:
            logging.warning(f"Tentativa {attempt} falhou: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise

# =============================
# Key Pair - SPFC
# =============================

def gen_private_key_spfc():
    passphrase = os.getenv("DB_PRIVATE_KEY_PASSPHRASE_SPFC")
    key_content = os.getenv("DB_PRIVATE_KEY_CONTENT_SPFC")

    # Reconstroi a chave privada, porque no .env tivemos que colocar quebras \n, para compartilhar de uma forma prática a private key.
    private_key_decoded = key_content.replace("\\n", "\n")

    private_key = serialization.load_pem_private_key(
        private_key_decoded.encode(),
        password=passphrase.encode(),
        backend=default_backend(),
    )

    # Snowflake exige formato DER PKCS8
    private_key_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return private_key_der

# =============================
# Conexão com SPFC
# =============================

def connect_dw_spfc(retries=10, delay=60):
    db_url = f"snowflake://{os.getenv('DB_USER_SPFC')}@{os.getenv('DB_HOST_SPFC')}/?warehouse={os.getenv('DB_WAREHOUSE_SPFC')}&database={os.getenv('DB_NAME_SPFC')}"

    for attempt in range(1, retries + 1):
        try:
            conn = create_engine(
                db_url, connect_args={"private_key": gen_private_key_spfc()}
            )

            with conn.connect() as sql:
                sql.execute(text("SELECT 1"))
                logging.info("Conectado ao DW com sucesso.")

            return conn

        except (OperationalError, DBAPIError, SnowflakeDatabaseError) as e:
            logging.warning(f"Tentativa {attempt} falhou: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise


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
                logging.info("Conectado ao DW")
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

