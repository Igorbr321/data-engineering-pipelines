import logging
import os
import time

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, DBAPIError
from snowflake.connector.errors import DatabaseError as SnowflakeDatabaseError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

load_dotenv() 

# =============================
# Key Pair Central
# =============================

def gen_private_key_central():
    passphrase = os.getenv("DB_PRIVATE_KEY_PASSPHRASE_CENTRAL")
    key_content = os.getenv("DB_PRIVATE_KEY_CONTENT_CENTRAL")

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
# Key Pair Lake
# =============================

def gen_private_key_lake():
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
# Conexão com Central
# =============================

def connect_dw_central(retries=1, delay=10):
    db_url = (
            f"snowflake://{os.getenv('DB_USER_CENTRAL')}@{os.getenv('DB_HOST_CENTRAL')}/?"
            f"warehouse={os.getenv('DB_WAREHOUSE_CENTRAL')}"
            f"&database={os.getenv('DB_NAME_CENTRAL')}"
            f"&schema={os.getenv('DB_SCHEMA_CENTRAL', 'PUBLIC')}"
        )

    for attempt in range(1, retries + 1):
        try:
            conn = create_engine(db_url, connect_args={"private_key": gen_private_key_central()}) # <--------------

            with conn.connect() as sql:
                sql.execute(text("SELECT 1"))
                logging.info("✅ Conectado ao DW com sucesso.")

            return conn

        except (OperationalError, DBAPIError, SnowflakeDatabaseError) as e:
            logging.warning(f"⚠️ Tentativa {attempt} falhou: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise

# =============================
# Conexão com Lake
# =============================

def connect_dw_lake(retries=1, delay=10):
    db_url = (
            f"snowflake://{os.getenv('DB_USER_SPFC')}@{os.getenv('DB_HOST_SPFC')}/?"
            f"warehouse={os.getenv('DB_WAREHOUSE_SPFC')}"
            f"&database={os.getenv('DB_NAME_SPFC')}"
            f"&schema={os.getenv('DB_SCHEMA_SPFC', 'PUBLIC')}"
        )

    for attempt in range(1, retries + 1):
        try:
            conn = create_engine(db_url, connect_args={"private_key": gen_private_key_lake()}) # <--------------

            with conn.connect() as sql:
                sql.execute(text("SELECT 1"))
                logging.info("✅ Conectado ao DW com sucesso.")

            return conn

        except (OperationalError, DBAPIError, SnowflakeDatabaseError) as e:
            logging.warning(f"⚠️ Tentativa {attempt} falhou: {e}")
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