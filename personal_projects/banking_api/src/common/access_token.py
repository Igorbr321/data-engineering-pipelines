#access_token.py
import requests


def access_token(api_key):
    response = requests.post(
        "https://api.pluggy.ai/connect_token",
        headers={
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        },
        json={},
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    connect_token = data["accessToken"]

    return connect_token