#transactions.py
from urllib.parse import parse_qs, urlparse

import requests


def get_transactions(api_key, account_id):
    transactions = []
    page = 1
    after = None

    while True:
        params = {
            "accountId": account_id,
        }

        if after:
            params["after"] = after

        response = requests.get(
            "https://api.pluggy.ai/v2/transactions",
            headers={
                "X-API-KEY": api_key,
            },
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])
        transactions.extend(results)

        next_url = data.get("next")

        if not next_url:
            break

        query_params = parse_qs(urlparse(next_url).query)
        after = query_params["after"][0]

        page += 1

    total_transactions = len(transactions)

    return transactions, page, total_transactions