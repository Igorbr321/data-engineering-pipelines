import os
import base64
import requests

from config.dotenv import load_dotenv


def credenciais_prd() -> tuple[str, str] | None:
    load_dotenv()
    client_id = os.getenv("CLIENT_ID_PRD")
    client_secret = os.getenv("CLIENT_SECRET_PRD")

    if not client_id or not client_secret:
        return None

    return client_id, client_secret


def get_token_prd() -> str:
    creds = credenciais_prd()
    if creds is None:
        raise ValueError("Credenciais não encontradas no .env")

    client_id, client_secret = creds
    url = "https://api.esm.com.br/authentication"

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers, timeout=30)
    response.raise_for_status()

    token = response.json()["access_token"]
    return token


def get_token_prd_base64() -> str:
    token_puro = get_token_prd()
    token_b64 = base64.b64encode(token_puro.encode()).decode()
    return token_b64
