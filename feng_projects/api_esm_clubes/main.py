import logging
import time

from common.utils import execution_time, save_logs
from config.logging_main import init_logging_main
from threads.threads import execute_all


def main():
    init_logging_main()
    start_time = time.time()
    error = None

    try:
        logging.info("Iniciando execução concorrente de pipelines")
        results = execute_all()

        sucesso = [n for n, ok in results.items() if ok]
        falha = [n for n, ok in results.items() if not ok]

        logging.info(f"Pipelines OK  : {sucesso}")
        logging.info(f"Pipelines ERRO: {falha}")

        if falha:
            error = f"Pipelines com erro: {falha}"

    except Exception as e:
        error = str(e)
        logging.exception("Erro na execução do processo")
        raise

    finally:
        exec_time = execution_time(start_time)
        logging.info(f"Fim do processo. Tempo de execução: {exec_time} minutos.")
        save_logs("API_ESM_SPFC", "API_ESM_CLUBES", exec_time, error)


if __name__ == "__main__":
    main()