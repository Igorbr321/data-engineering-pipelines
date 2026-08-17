import json
import logging
import tempfile
import time
import os
import pandas as pd

from google.cloud import bigquery
from google.oauth2 import service_account
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, DBAPIError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from snowflake.connector.errors import DatabaseError as SnowflakeDatabaseError
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import pd_writer

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

    db_url = f"snowflake://{os.getenv(f'USER_DW_SPFC')}:{os.getenv(f'PASSWORD_DW_SPFC')}@{os.getenv(f'HOST_DW_SPFC')}/{os.getenv(f'NAME_DW_SPFC')}?warehouse={os.getenv(f'WAREHOUSE_DW_SPFC')}"

    for attempt in range(1, retries + 1):
        try:
            conn = create_engine(db_url)
            with conn.connect() as sql:
                sql.execute(text("SELECT 1"))
                logging.info("🔵 Conectado ao DW com sucesso.")
            return conn
        except (OperationalError, DBAPIError, SnowflakeDatabaseError) as e:
            logging.warning(f"⚠️ Tentativa {attempt} falhou: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise

# =============================
# Conexão com Bigquery
# =============================

def connect_bigquery(credential_env_var):
    # pega a string JSON da variável de ambiente
    credentials_str = os.getenv(credential_env_var)
    if not credentials_str:
        raise ValueError(f"Variável {credential_env_var} não encontrada")

    # corrige quebras de linha se tiver
    credentials_str = credentials_str.replace("\n", "@BREAK@")
    credentials = json.loads(credentials_str)
    credentials["private_key"] = credentials["private_key"].replace("@BREAK@", "\n")

    # salva em arquivo temporário
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        json.dump(credentials, temp_file)
        temp_file_path = temp_file.name

    # cria client passando explicitamente as credenciais
    creds = service_account.Credentials.from_service_account_file(temp_file_path)
    client = bigquery.Client(credentials=creds, project=creds.project_id)

    logging.info("Conectado ao BigQuery")

    return client

# =============================
# Conexão para armazenar log
# =============================

def save_logs(program, table, execution_time, error):
    from datetime import datetime

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

# =================================
# Log da pipeline
# =================================

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
    logging.info("### START ###")

# =================================
# Tempo de execução da pipeline
# =================================

def execution_time(start_time):
    import time

    execution_time = time.time() - start_time
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)

    return round(minutes + (seconds / 100), 2)
