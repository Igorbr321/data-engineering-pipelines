import logging
import time

from extract_dim_calendario_fla import extract_dim_calendario_fla
from insert_lake_vasco_spfc import inserir_lake_vasco, inserir_lake_spfc
from utils import init_logging, execution_time


def main():
    init_logging()
    start_time = time.time()
    error = "N"

    try:
        logging.info("Iniciando extração da dim_calendário do Lake Flamengo.")
        df = extract_dim_calendario_fla()

        inserir_lake_vasco(df)
        inserir_lake_spfc(df)

    except Exception as e:
        error = "S"
        logging.critical(f"OCORREU UM ERRO: {e}")

    finally:
        logging.info(f"ERROR_FLAG={error}")
        logging.info(f"Tempo de execução: {execution_time(start_time)}")


if __name__ == "__main__":
    main()

