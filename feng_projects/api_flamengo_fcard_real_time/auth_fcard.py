import os
from dotenv import load_dotenv

load_dotenv()

def get_token():
    token = os.getenv("TOKEN_FUTEBOLCARD")

    if not token:
        raise ValueError("TOKEN_FUTEBOLCARD não encontrado no .env")

    return token


def get_headers():
    return {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }