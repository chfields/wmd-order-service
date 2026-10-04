"""Tests use a real Postgres: DATABASE_URL (a Wardby coding run sets it) or local docker.
catalog-service and notification-service are fakes that record what they were sent."""

import json
import os
import uuid

import httpx
import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg import sql

from app.db import Database
from app.main import create_app

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://wmd:wmd@localhost:55440/wmd")
PRICES = {"sku-coffee": ("Cold Brew Coffee", 899), "sku-bagels": ("Everything Bagels", 649)}


class FakeCatalog:
    """Reserves anything in PRICES; `short` products are out of stock."""

    def __init__(self) -> None:
        self.calls: list[httpx.Request] = []
        self.short: set[str] = set()
        self.down = False

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.calls.append(request)
        if self.down:
            raise httpx.ConnectError("catalog down")
        body = json.loads(request.content)
        lines = []
        for item in body["items"]:
            product = item["productId"]
            if product not in PRICES:
                return httpx.Response(
                    422, json={"error": {"code": "unknown_product", "message": f"No {product}."}}
                )
            if product in self.short:
                return httpx.Response(
                    409, json={"error": {"code": "unavailable", "message": f"No {product}."}}
                )
            name, price = PRICES[product]
            lines.append(
                {
                    "productId": product,
                    "name": name,
                    "quantity": item["quantity"],
                    "priceCents": price,
                }
            )
        total = sum(line["quantity"] * line["priceCents"] for line in lines)
        return httpx.Response(
            201,
            json={
                "id": str(uuid.uuid4()),
                "orderRef": body["orderRef"],
                "lines": lines,
                "totalCents": total,
            },
        )


class FakeNotifications:
    def __init__(self) -> None:
        self.calls: list[httpx.Request] = []
        self.status = 201

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.calls.append(request)
        return httpx.Response(self.status, json={"id": str(uuid.uuid4())})


@pytest.fixture
def database():
    db = Database(DATABASE_URL, f"orders_test_{uuid.uuid4().hex[:12]}")
    yield db
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        conn.execute(sql.SQL("drop schema if exists {} cascade").format(sql.Identifier(db.schema)))


@pytest.fixture
def catalog():
    return FakeCatalog()


@pytest.fixture
def notifications():
    return FakeNotifications()


@pytest.fixture
def client(database, catalog, notifications):
    app = create_app(
        database,
        catalog=httpx.Client(
            base_url="http://catalog", transport=httpx.MockTransport(catalog.handle)
        ),
        notifications=httpx.Client(
            base_url="http://notifications", transport=httpx.MockTransport(notifications.handle)
        ),
    )
    with TestClient(app) as test_client:
        yield test_client
