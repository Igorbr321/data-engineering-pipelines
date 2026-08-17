import logging 
import time

from datetime import datetime, timedelta
from pipelines.users.extracao_users import extracao_usuarios
from pipelines.users.insert_users import inserir_usuarios_esm
from config.logging_pipelines import init_logging
from common.utils import execution_time, save_logs

def main():
    init_logging('users')
    start_time = time.time()
    error = None


    # Reprocessamento de datas específicas
    # date_start = "2026-03-17"
    # date_end = "2026-03-18"

    # Processamento diário
    date_ref = datetime.now().date()
    date_start = (date_ref - timedelta(days=1)).strftime("%Y-%m-%d")
    date_end = date_ref.strftime("%Y-%m-%d")

    per_page = 100

    try:
        df_usuarios = extracao_usuarios(
            date_start=date_start,
            date_end=date_end,
            per_page=per_page,
        )

        total = len(df_usuarios)
        logging.info(f"🟡 [USERS] - Total extraído: {total}")

        if not df_usuarios.empty:
            inserir_usuarios_esm(
                df_usuarios,
                date_start=date_start,
                date_end=date_end,
            )
            logging.info("🟡 [USERS] - Inserção finalizada com sucesso.")
        else:
            logging.warning("🟡 [USERS] - Nenhum registro retornado. Nada para inserir.")

        logging.info(f"🟡 [USERS] OK (total={total})")

    except Exception as e:
        error = str(e)
        logging.exception("Erro na execução do processo")
        raise

    finally:
        exec_time = execution_time(start_time)
        logging.info(f"🟡 [USERS] - Fim do processo. Tempo de execução: {exec_time} minutos.")
        #save_logs("API_ESM_SPFC", "API_ESM_CLUBES", exec_time, error)

    logging.info("🟡 [USERS] - Finalizado.")


if __name__ == "__main__":
    main()
