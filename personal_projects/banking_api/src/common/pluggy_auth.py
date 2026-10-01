#pluggy_auth.py
import os
import requests

from dotenv import load_dotenv

load_dotenv()


def pluggy_auth():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    response = requests.post(
        "https://api.pluggy.ai/auth",
        json={
            "clientId": client_id,
            "clientSecret": client_secret,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    api_key = data["apiKey"]

    return api_key