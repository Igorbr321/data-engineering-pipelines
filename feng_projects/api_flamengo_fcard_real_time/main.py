import logging
import time

from dotenv import load_dotenv

from utils import (
    init_logging,
    execution_time,
)

from orchestrator import (
    executar_real_time,
    executar_reprocessamento_manual,
    executar_reprocessamento_scheduler,
)


# ===========================================
# CONFIGURAÇÃO
# ===========================================

"""
MODOS:

1 = REAL_TIME
2 = REPROCESSAMENTO_MANUAL
3 = REPROCESSAMENTO_SCHEDULER
"""

MODO_EXECUCAO = 3


# ===========================================
# MAIN
# ===========================================

def main():

    load_dotenv()

    init_logging()

    start_time = time.time()

    logging.info("")
    logging.info("=" * 90)

    # ===========================================
    # NOME DO MODO
    # ===========================================

    if MODO_EXECUCAO == 1:
        nome_modo = "REAL_TIME"

    elif MODO_EXECUCAO == 2:
        nome_modo = "REPROCESSAMENTO_MANUAL"

    elif MODO_EXECUCAO == 3:
        nome_modo = "REPROCESSAMENTO_SCHEDULER"

    else:
        nome_modo = "DESCONHECIDO"

    logging.info(
        f"Iniciando processo FCARD "
        f"| modo={nome_modo}"
    )

    logging.info("=" * 90)

    try:

        # ===========================================
        # REALTIME
        # ===========================================

        if MODO_EXECUCAO == 1:

            executar_real_time()

        # ===========================================
        # REPROCESSAMENTO MANUAL
        # ===========================================

        elif MODO_EXECUCAO == 2:

            df = executar_reprocessamento_manual()

            logging.info(
                f"[MAIN] total linhas={len(df)}"
            )

        # ===========================================
        # REPROCESSAMENTO SCHEDULER
        # ===========================================

        elif MODO_EXECUCAO == 3:

            df = executar_reprocessamento_scheduler()

            logging.info(
                f"[MAIN] total linhas={len(df)}"
            )

        # ===========================================
        # MODO INVÁLIDO
        # ===========================================

        else:

            raise ValueError(
                f"Modo inválido: {MODO_EXECUCAO}"
            )

    except Exception as e:

        logging.critical(
            f"Ocorreu um erro: {e}"
        )

        raise

    finally:

        exec_time = execution_time(start_time)

        logging.info(
            f"Fim do processo. "
            f"Tempo de execução: {exec_time} minutos."
        )


# ===========================================
# START
# ===========================================

if __name__ == "__main__":
    main()