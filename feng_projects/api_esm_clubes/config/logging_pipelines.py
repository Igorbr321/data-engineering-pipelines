import logging
import warnings
from sqlalchemy.exc import SAWarning
from pathlib import Path

# nomes das pastas em pipelines/
pipeline_names = [
    "orders",
    "users",
]

def init_logging(pipeline_name: str):
    # validação rápida
    if pipeline_name not in pipeline_names:
        raise ValueError(f"Pipeline desconhecida: {pipeline_name!r}")

    # ignora warning específico do SQLAlchemy
    warnings.filterwarnings(
        "ignore",
        category=SAWarning,
        message="The GenericFunction 'flatten' is already registered and is going to be overridden."
    )

    # monta caminho para pipelines/<pipeline_name>/
    project_root = Path(__file__).parents[1]
    log_dir = project_root / "pipelines" / pipeline_name
    log_dir.mkdir(parents=True, exist_ok=True)

    # define arquivo de log dentro da própria pasta da pipeline
    log_file = log_dir / f"{pipeline_name}.log"

    # configura logger raiz para gravar neste arquivo
    logging.basicConfig(
        filename=str(log_file),
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )

    # reduz verbosidade do conector Snowflake
    logging.getLogger("snowflake.connector").setLevel(logging.WARNING)
