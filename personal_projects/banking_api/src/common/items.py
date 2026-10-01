#items.py
import time
import requests


def create_item(api_key, connector_id, user):
    response = requests.post(
        "https://api.pluggy.ai/items",
        headers={
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        },
        json={
            "connectorId": connector_id,
            "parameters": {
                "user": user,
                "password": "password-ok",
            },
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_item(api_key, item_id):
    response = requests.get(
        f"https://api.pluggy.ai/items/{item_id}",
        headers={
            "X-API-KEY": api_key,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def wait_for_item(api_key, item_id):
    while True:
        item = get_item(
            api_key=api_key,
            item_id=item_id,
        )

        status = item["status"]

        if status == "UPDATED":
            return item

        if status == "LOGIN_ERROR":
            raise RuntimeError("Item authentication failed.")

        if status == "ERROR":
            raise RuntimeError(
                f"Item update failed: {item.get('error')}"
            )

        time.sleep(2)