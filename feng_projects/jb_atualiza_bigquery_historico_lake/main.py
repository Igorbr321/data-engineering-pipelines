import logging
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from functions import pipeline
from utils import execution_time, init_logging, save_logs


def main():
    try:
        load_dotenv()
        init_logging()

        error = "N"
        start_time = time.time()

        #save_logs("BIGQUERY", "JB_ATUALIZA_BIGQUERY_HISTORICO_LAKE", 0, error)

        start_date = (datetime.now() - timedelta(days=2)).date()
        end_date = (datetime.now() - timedelta(days=2)).date()

        # para carregar um periodo especifico habilite isso
        # start_date = date(2025, 5, 19)
        # end_date = date(2026, 6, 22)

        teams = [
            ("SÃO PAULO", "351961152"),   # 2025-5-19 inicio projeto
        ]

        tables = [
            "bigquery_base",
            "bigquery_automation_crm"
        ]

        while start_date <= end_date:
            date_str = start_date.strftime("%Y-%m-%d")

            logging.info(f"Data: {date_str}")

            with ThreadPoolExecutor(max_workers=9) as executor:
                threads = [
                    executor.submit(pipeline, team, property_id, date_str, table)
                    for team, property_id in teams
                    for table in tables
                ]

                for thread in as_completed(threads):
                    thread.result()

            start_date += timedelta(days=1)

    except Exception as e:
        logging.info(e)
        error = "S"

    finally:
        exec_time = execution_time(start_time)

        logging.info(f"Fim do processo. Tempo de execução: {exec_time} minutos.")

        #save_logs("BIGQUERY", "JB_ATUALIZA_BIGQUERY_HISTORICO_LAKE", exec_time, error)


if __name__ == "__main__":
    main()
