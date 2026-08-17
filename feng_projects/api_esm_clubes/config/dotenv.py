from pathlib import Path

from dotenv import load_dotenv as _load_dotenv

def load_dotenv():
    """
    Carrega o arquivo config/.env e exporta suas chaves para as variáveis de ambiente.
    Lança FileNotFoundError se o arquivo não for encontrado.
    """
    # Pasta onde este arquivo está (config/)
    config_dir = Path(__file__).parent
    env_path = config_dir / ".env"

    if not env_path.is_file():
        raise FileNotFoundError(f".env não encontrado em {env_path}")

    # Carrega e sobrescreve variáveis já existentes, se houver
    _load_dotenv(dotenv_path=str(env_path), override=True)
