import os 
import time
import logging
import pandas as pd 

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, DBAPIError
from snowflake.connector.errors import DatabaseError as SnowflakeDatabaseError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

load_dotenv()

# =============================
# Key Pair
# =============================

def gen_private_key():
    passphrase = os.getenv("DB_PRIVATE_KEY_PASSPHRASE")
    key_content = os.getenv("DB_PRIVATE_KEY_CONTENT")

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


# ================================
# Conexão com Lake SPFC
# ================================

def connect_dw_lake_spfc(retries=2, delay=10):

    db_url = (
        f"snowflake://{os.getenv('DB_USER')}@{os.getenv('DB_HOST')}/?"
        f"warehouse={os.getenv('DB_WAREHOUSE')}"
        f"&database={os.getenv('DB_NAME')}"
        f"&schema={os.getenv('DB_SCHEMA', 'PUBLIC')}"
    )

    for attempt in range(1, retries + 1):
        try:
            conn = create_engine(db_url, connect_args={"private_key": gen_private_key()}) # <--------------

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
# Conexão para armazenar log
# =============================

def save_logs(program, table, execution_time, error):
    from datetime import datetime

    logs = ""

    # Ler o conteúdo do arquivo de log
    with open("threads.log", "r", encoding="utf-8") as log_file:
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

    conn = connect_dw_lake_spfc()
    with conn.connect() as sql:
        df.to_sql(
            "logs_processos",
            sql,
            schema="BRONZE",
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

