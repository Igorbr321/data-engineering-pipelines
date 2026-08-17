import os
from dotenv import load_dotenv

load_dotenv()

def get_token_vasco() -> str:

    token = os.getenv("AUTHORIZATION_VASCO")
    if not token:
        raise ValueError("Token AUTHORIZATION_VASCO não encontrado no .env")
    return token
