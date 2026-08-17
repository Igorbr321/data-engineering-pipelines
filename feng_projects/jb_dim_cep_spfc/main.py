import logging
import time

from utils import execution_time, init_logging
from extract_dim_cep_central import extract_dim_cep_central
from load_dim_cep_lake_spfc import load_dim_cep_lake


def main():
    init_logging()
    start_time = time.time()
    error = None

    try:
        df_dim_cep = extract_dim_cep_central()

        if df_dim_cep.empty:
            logging.warning("⚠️ DataFrame vazio. Nenhum dado para carregar no LAKE.")
        else:
            batch_size = 100000

            logging.info(f"Total de registros encontrados: {len(df_dim_cep)}")

            for i in range(0, len(df_dim_cep), batch_size):
                lote = df_dim_cep.iloc[i:i + batch_size]

                logging.info(
                    f"Carregando lote {i // batch_size + 1} "
                    f"({len(lote)} registros)"
                )

                load_dim_cep_lake(lote)

    except Exception as e:
        error = str(e)
        logging.exception(error)
        raise

    finally:
        exec_time = execution_time(start_time)
        logging.info(f"✅ Fim do processo. Tempo de execução: {exec_time} minutos.")


if __name__ == "__main__":
    main()