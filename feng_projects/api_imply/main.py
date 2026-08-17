import logging
import time

from datetime import datetime
from utils import execution_time, init_logging, save_logs
from extract import extracao_datalake_vasco
from transform import transform_df
from insert import inserir_lake_fla 


def main():
    init_logging()
    start_time = time.time()
    error = None

    try:
        # Reprocessamento de datas específicas
        date_start = "2026-06-24"
        date_end = "2026-08-05"

        # Processamento diário
        # date_ref = datetime.now().date()
        # date_start = date_ref.strftime("%Y-%m-%d")
        # date_end = date_ref.strftime("%Y-%m-%d")

        max_results = 100000

        # Extração dos dados
        logging.info(f"🟡 [VASCO] - Iniciando processo para o período: {date_start} a {date_end}")
        df = extracao_datalake_vasco(
            date_start=date_start,
            date_end=date_end,
            max_results=max_results,
        )
        logging.info(f"🟡 [VASCO] - Registros extraídos: {len(df)}")

        # Transformação dos dados
        df = transform_df(df)
        logging.info("🟡 [VASCO] - Transformação finalizada")

        df.to_csv("vasco_extracted_transformed.csv", index=False, encoding="utf-8")

        # df_col = df.columns.tolist()
        # logging.info(f"🟡 [VASCO] - Colunas extraídas: {df_col}")

        # Inserção dos dados
        logging.info("🟡 [VASCO] - Iniciando inserção")
        inserir_lake_fla(df=df, date_start=date_start, date_end=date_end)
        logging.info("🟡 [VASCO] - Inserção finalizada")

    except Exception as e:
        error = str(e)
        logging.exception(error)
        raise

    finally:
        exec_time = execution_time(start_time)
        logging.info(f"✅ Fim do processo. Tempo de execução: {exec_time} minutos.")
        # save_logs("VASCO", "CARGA_FT_COMPRAINGRESSO_FAKE", exec_time, error)


if __name__ == "__main__":
    main()
