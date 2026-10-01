#accounts.py
import requests


def get_accounts(api_key, item_id):
    response = requests.get(
        "https://api.pluggy.ai/accounts",
        headers={
            "X-API-KEY": api_key,
        },
        params={
            "itemId": item_id,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()
