import logging

from datetime import datetime, timedelta

from pipelines.orders.extracao_orders import extracao_orders
from pipelines.orders.insert_orders import inserir_ordens_esm
from config.logging_pipelines import init_logging


def main():

    init_logging("orders")

    # ==========================================
    # PROCESSAMENTO DIÁRIO
    # ==========================================
    data_atual = datetime.now().date() - timedelta(days=1)
    data_final = datetime.now().date()

    # ==========================================
    # REPROCESSAMENTO
    # ==========================================
    # date_start = "2026-05-28"
    # date_end = "2026-05-28"

    # data_atual = datetime.strptime(date_start, "%Y-%m-%d").date()
    # data_final = datetime.strptime(date_end, "%Y-%m-%d").date()

    per_page = 100

    try:

        while data_atual <= data_final:

            data_ref = data_atual.strftime("%Y-%m-%d")

            logging.info(
                f"🟢 [ORDERS] - PROCESSANDO {data_ref}"
            )

            # ==========================================
            # EXTRAÇÃO
            # ==========================================
            df_orders = extracao_orders(
                date_start=data_ref,
                date_end=data_ref,
                per_page=per_page,
            )

            total = len(df_orders)

            logging.info(
                f"🟢 [ORDERS] - Total extraído em {data_ref}: {total}"
            )

            # ==========================================
            # INSERÇÃO
            # ==========================================
            if not df_orders.empty:

                inserir_ordens_esm(
                    df_orders,
                    date_start=data_ref,
                    date_end=data_ref,
                )

                logging.info(
                    f"🟢 [ORDERS] - Inserção concluída em {data_ref}"
                )

            else:

                logging.warning(
                    f"🟡 [ORDERS] - Nenhum registro encontrado em {data_ref}"
                )

            # próximo dia
            data_atual += timedelta(days=1)

        logging.info(
            "🟢 [ORDERS] - Processamento finalizado"
        )

    except Exception:

        logging.exception(
            "🔴 [ORDERS] - FALHOU"
        )

        raise

    logging.info(
        "🔵 [ORDERS] - Finalizado."
    )

if __name__ == "__main__":
    main()