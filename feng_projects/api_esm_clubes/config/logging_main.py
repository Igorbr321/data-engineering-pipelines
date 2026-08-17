import logging
import warnings
from pathlib import Path
from sqlalchemy.exc import SAWarning

def init_logging_main():
    warnings.filterwarnings(
        "ignore",
        category=SAWarning,
        message="The GenericFunction 'flatten' is already registered and is going to be overridden."
    )

    project_root = Path(__file__).parent.parent
    log_file = project_root / "threads.log"

    logging.basicConfig(
        filename=str(log_file),
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )

    logging.getLogger("snowflake.connector").setLevel(logging.WARNING)
