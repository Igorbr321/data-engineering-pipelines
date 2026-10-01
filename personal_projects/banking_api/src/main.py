#main.py
import logging
import time

from common.access_token import access_token
from common.items import create_item, wait_for_item
from common.pluggy_auth import pluggy_auth
from common.utils import execution_time, logging_config

from ingestion.accounts import get_accounts
from ingestion.transactions import get_transactions

def main():
    logging_config()
    start_time = time.time()


    try:
        logging.info("Pipeline execution started.")

        # Authentication
        api_key = pluggy_auth()
        logging.info("API Key generated successfully.")

        access_token(api_key)
        logging.info("Access Token generated successfully.")

        # Create Pluggy Item
        item = create_item(
            api_key=api_key,
            connector_id=2,
            user="user-ok-perf-1000x",
        )
        logging.info("Item created successfully.")
        logging.info("Item ID: %s", item["id"])

        # Wait for Item synchronization
        item = wait_for_item(
            api_key=api_key,
            item_id=item["id"],
        )
        logging.info("Item synchronized successfully.")

        # Extract Accounts
        accounts = get_accounts(
            api_key=api_key,
            item_id=item["id"],
        )
        
        logging.info("Accounts extracted successfully.")
        logging.info("Total accounts: %s", accounts["total"])

        #Get transactions 
        account_id = accounts["results"][0]["id"]

        transactions, total_pages, total_transactions = get_transactions(
            api_key=api_key,
            account_id=account_id,
        )

        logging.info("Transactions extracted successfully.")
        logging.info("Transaction pages: %s", total_pages)
        logging.info("Total transactions: %s", total_transactions)

    except Exception as e:
        logging.error("Pipeline execution failed: %s", e)

    finally:
        elapsed_time = execution_time(start_time)
        logging.info("Execution time: %.2f minutes", elapsed_time)


if __name__ == "__main__":
    main()
