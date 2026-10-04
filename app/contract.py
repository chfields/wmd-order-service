"""Print this service's OpenAPI contract: python -m app.contract > openapi.json"""

import json

import httpx

from app.db import Database
from app.main import create_app


def contract() -> dict:
    return create_app(
        Database("postgresql://contract-only", "orders"),
        catalog=httpx.Client(),
        notifications=httpx.Client(),
        migrate=False,
    ).openapi()


if __name__ == "__main__":
    print(json.dumps(contract(), indent=2, sort_keys=True))
