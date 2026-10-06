"""order-service: carts become orders. Reserves stock with catalog-service, then confirms the
order once notification-service has told the customer."""

from __future__ import annotations

import logging
import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Literal

import httpx
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, field_validator

from app.db import Database, database_from_env
from app.observability import ApiError, configure_logging, install, outbound_headers

SERVICE = "order-service"
log = logging.getLogger("wmd.orders")
DeliveryWindow = Literal["morning", "afternoon", "evening"]


class OrderItem(BaseModel):
    productId: str = Field(min_length=1, max_length=64)
    quantity: int = Field(ge=1, le=100)


class OrderRequest(BaseModel):
    userId: str = Field(min_length=1, max_length=64)
    items: list[OrderItem] = Field(min_length=1, max_length=50)
    giftMessage: str | None = Field(default=None, json_schema_extra={"maxLength": 200})
    deliveryWindow: DeliveryWindow | None = "morning"

    @field_validator("deliveryWindow", mode="before")
    @classmethod
    def validate_delivery_window(cls, value):
        if value is not None and value not in ("morning", "afternoon", "evening"):
            raise ApiError(
                422,
                "invalid_delivery_window",
                "Delivery window must be morning, afternoon or evening.",
            )
        return value


class OrderLine(BaseModel):
    productId: str
    name: str
    quantity: int
    priceCents: int


class Order(BaseModel):
    id: str
    userId: str
    status: Literal["pending", "confirmed"]
    totalCents: int
    lines: list[OrderLine]
    giftMessage: str | None
    deliveryWindow: DeliveryWindow
    createdAt: datetime
    updatedAt: datetime


def _client(env: str) -> httpx.Client:
    return httpx.Client(base_url=os.environ[env], timeout=5.0)


def create_app(
    db: Database | None = None,
    *,
    catalog: httpx.Client | None = None,
    notifications: httpx.Client | None = None,
    migrate: bool = True,
) -> FastAPI:
    database = db or database_from_env("orders")
    catalog_client = catalog or _client("CATALOG_URL")
    notification_client = notifications or _client("NOTIFICATION_URL")

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        if migrate:
            database.migrate()
        yield

    app = FastAPI(title="wmd order-service", version="1.0.0", lifespan=lifespan)
    install(app, database.ping)

    def load(conn, order_id: str) -> Order | None:
        order = conn.execute(
            "select id, user_id, status, total_cents, gift_message, delivery_window,"
            " created_at, updated_at"
            " from orders where id = %s",
            (order_id,),
        ).fetchone()
        if order is None:
            return None
        lines = conn.execute(
            "select product_id, name, quantity, price_cents from order_lines"
            " where order_id = %s order by product_id",
            (order_id,),
        ).fetchall()
        return Order(
            id=str(order["id"]),
            userId=order["user_id"],
            status=order["status"],
            totalCents=order["total_cents"],
            lines=[
                OrderLine(
                    productId=line["product_id"],
                    name=line["name"],
                    quantity=line["quantity"],
                    priceCents=line["price_cents"],
                )
                for line in lines
            ],
            giftMessage=order["gift_message"],
            deliveryWindow=order["delivery_window"],
            createdAt=order["created_at"],
            updatedAt=order["updated_at"],
        )

    def reserve(order_id: str, request: OrderRequest) -> dict:
        try:
            response = catalog_client.post(
                "/v1/reservations",
                json={"orderRef": order_id, "items": [i.model_dump() for i in request.items]},
                headers=outbound_headers(),
            )
        except httpx.HTTPError as error:
            raise ApiError(502, "catalog_unavailable", "The catalog can't be reached.") from error
        if response.status_code in (409, 422):
            error = response.json()["error"]
            raise ApiError(response.status_code, error["code"], error["message"])
        if response.status_code != 201:
            raise ApiError(502, "catalog_unavailable", "The catalog couldn't reserve stock.")
        return response.json()

    def notify(order: Order) -> bool:
        payload = {
            "userId": order.userId,
            "orderId": order.id,
            "kind": "order_confirmed",
            "totalCents": order.totalCents,
            "deliveryWindow": order.deliveryWindow,
        }
        if order.giftMessage is not None:
            # Forward-compatible: notification-service currently ignores giftMessage; it will be
            # visible once that service accepts and shows it in a separate change.
            payload["giftMessage"] = order.giftMessage
        try:
            response = notification_client.post(
                "/v1/notifications",
                json=payload,
                headers=outbound_headers(),
            )
        except httpx.HTTPError:
            log.warning("notification failed", extra={"fields": {"orderId": order.id}})
            return False
        if response.status_code not in (200, 201):
            log.warning(
                "notification refused",
                extra={"fields": {"orderId": order.id, "status": response.status_code}},
            )
            return False
        return True

    @app.post("/v1/orders", response_model=Order, status_code=201)
    def place(request: OrderRequest) -> Order:
        delivery_window: DeliveryWindow = request.deliveryWindow or "morning"
        gift_message = request.giftMessage.strip() if request.giftMessage is not None else None
        if not gift_message:
            gift_message = None
        if gift_message is not None and len(gift_message) > 200:
            raise ApiError(
                422,
                "invalid_gift_message",
                "Gift messages can be at most 200 characters.",
            )
        order_id = str(uuid.uuid4())
        reservation = reserve(order_id, request)
        with database.connect() as conn:
            conn.execute(
                "insert into orders (id, user_id, status, total_cents, gift_message,"
                " delivery_window)"
                " values (%s, %s, 'pending', %s, %s, %s)",
                (
                    order_id,
                    request.userId,
                    reservation["totalCents"],
                    gift_message,
                    delivery_window,
                ),
            )
            for line in reservation["lines"]:
                conn.execute(
                    "insert into order_lines (order_id, product_id, name, quantity, price_cents)"
                    " values (%s, %s, %s, %s, %s)",
                    (
                        order_id,
                        line["productId"],
                        line["name"],
                        line["quantity"],
                        line["priceCents"],
                    ),
                )
            order = load(conn, order_id)
        log.info("order placed", extra={"fields": {"orderId": order_id}})
        if notify(order):
            with database.connect() as conn:
                conn.execute(
                    "update orders set status = 'confirmed', updated_at = now() where id = %s",
                    (order_id,),
                )
                order = load(conn, order_id)
            log.info("order confirmed", extra={"fields": {"orderId": order_id}})
        return order

    @app.get("/v1/orders/{order_id}", response_model=Order)
    def get_order(order_id: uuid.UUID) -> Order:
        with database.connect() as conn:
            order = load(conn, str(order_id))
        if order is None:
            raise ApiError(404, "unknown_order", f"No order {order_id}.")
        return order

    @app.get("/v1/orders", response_model=list[Order])
    def list_for_user(
        userId: str = Query(min_length=1, max_length=64),  # noqa: N803 - API field name
    ) -> list[Order]:
        with database.connect() as conn:
            ids = conn.execute(
                "select id from orders where user_id = %s order by created_at desc limit 50",
                (userId,),
            ).fetchall()
            return [load(conn, str(row["id"])) for row in ids]

    return app


def main() -> FastAPI:
    """uvicorn entrypoint: `uvicorn app.main:main --factory`."""
    configure_logging(SERVICE)
    return create_app()
