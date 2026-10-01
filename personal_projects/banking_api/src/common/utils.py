#utils.py
import logging
import os
import psycopg2
import time

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# Connect to PostgreSQL database

def connect_postgresql():
    """
    Connect and test a PostgreSQL database connection.
    """
    try:
        logging.info("Connecting to PostgreSQL database...")

        connection = psycopg2.connect(
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

        if result == (1,):
            logging.info("PostgreSQL connection successful.")
            return connection

        logging.error("PostgreSQL connection test failed.")
        connection.close()
        return None

    except psycopg2.Error as error:
        logging.error("PostgreSQL connection failed: %s", error)
        return None


# Logging configuration

def logging_config():
    """
    Configure logging settings for the application.
    """

    src_path = Path(__file__).resolve().parent.parent
    log_path = src_path / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, mode="w"),
        ],
    )

# Execution time calculation

def execution_time(start_time):

    execution_time = time.time() - start_time
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)

    return round(minutes + (seconds / 100), 2)