import os


def get_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Environment variable '{name}' is not set.")

    return value
