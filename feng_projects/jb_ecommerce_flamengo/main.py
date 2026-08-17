import logging
import time

from utils import init_logging, execution_time

from extract_transform_master import extract_master, transform_master
from insert_master import inserir_master

from extract_transform_pedidos import extract_pedidos, transform_pedidos
from insert_pedidos import inserir_pedidos


def main():
    init_logging()
    start_time = time.time()

    try:
        logging.info("🚀 [PIPELINE] Iniciando execução do pipeline.")

        # -------------------
        # MASTER
        # -------------------
        logging.info("🔵 [MASTER] Iniciando etapa (extract -> transform)")
        df_master = extract_master(
            r"C:\Users\igor.pedro\Downloads\Igor_feng\to_do\ecommerce_flamengo\data_raw\masterdata_raw\Masterdata.csv"
        )
        df_master = transform_master(df_master)
        logging.info(f"🔵 [MASTER] Finalizado: {df_master.shape[0]} linhas, {df_master.shape[1]} colunas")

        inserir_master(df_master)


        # -------------------
        # PEDIDOS
        # -------------------
        logging.info("🟢 [PEDIDOS] Iniciando etapa (extract -> transform)")
        df_pedidos = extract_pedidos(
            path_jan_jun=r"C:\Users\igor.pedro\Downloads\Igor_feng\to_do\ecommerce_flamengo\data_raw\pedidos_raw\Jan-Jun 2025.csv",
            path_jul_dez=r"C:\Users\igor.pedro\Downloads\Igor_feng\to_do\ecommerce_flamengo\data_raw\pedidos_raw\Jul-Dez 2025.csv",
            path_jan_2026=r"C:\Users\igor.pedro\Downloads\Igor_feng\to_do\ecommerce_flamengo\data_raw\pedidos_raw\Jan 2026.csv",
        )
        df_pedidos = transform_pedidos(df_pedidos)

        logging.info(f"🟢 [PEDIDOS] Finalizado: {df_pedidos.shape[0]} linhas, {df_pedidos.shape[1]} colunas")

        inserir_pedidos(df_pedidos)


        logging.info("🎯 [PIPELINE] Execução finalizada com sucesso.")


    except Exception as e:
        logging.exception(f"❌ [PIPELINE] Erro na execução: {e}")
        raise


    finally:
        logging.info(f"⏱️ [PIPELINE] Tempo total de execução: {execution_time(start_time)}")


if __name__ == "__main__":
    main()