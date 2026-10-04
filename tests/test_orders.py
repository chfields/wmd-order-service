import json

CART = {
    "userId": "user-1",
    "items": [
        {"productId": "sku-coffee", "quantity": 2},
        {"productId": "sku-bagels", "quantity": 1},
    ],
}


def test_places_an_order_and_confirms_it_once_the_customer_is_notified(
    client, catalog, notifications
):
    response = client.post("/v1/orders", json=CART)
    assert response.status_code == 201
    order = response.json()
    assert order["status"] == "confirmed"
    assert order["totalCents"] == 2 * 899 + 649
    assert [line["productId"] for line in order["lines"]] == ["sku-bagels", "sku-coffee"]

    assert json.loads(catalog.calls[0].content)["orderRef"] == order["id"]
    assert json.loads(notifications.calls[0].content) == {
        "userId": "user-1",
        "orderId": order["id"],
        "kind": "order_confirmed",
        "totalCents": 2 * 899 + 649,
    }
    assert client.get(f"/v1/orders/{order['id']}").json() == order


def test_forwards_the_correlation_id_to_both_services(client, catalog, notifications):
    client.post("/v1/orders", json=CART, headers={"x-correlation-id": "journey-42"})
    assert catalog.calls[0].headers["x-correlation-id"] == "journey-42"
    assert notifications.calls[0].headers["x-correlation-id"] == "journey-42"


def test_keeps_the_order_pending_when_the_notification_fails(client, notifications):
    notifications.status = 503
    order = client.post("/v1/orders", json=CART).json()
    assert order["status"] == "pending"
    assert client.get(f"/v1/orders/{order['id']}").json()["status"] == "pending"


def test_passes_on_out_of_stock_and_unknown_products_creating_nothing(client, catalog):
    catalog.short.add("sku-bagels")
    short = client.post("/v1/orders", json=CART)
    assert short.status_code == 409
    assert short.json()["error"]["code"] == "unavailable"

    unknown = client.post(
        "/v1/orders",
        json={"userId": "user-1", "items": [{"productId": "sku-caviar", "quantity": 1}]},
    )
    assert unknown.status_code == 422
    assert unknown.json()["error"]["code"] == "unknown_product"
    assert client.get("/v1/orders", params={"userId": "user-1"}).json() == []


def test_reports_a_catalog_outage_as_502(client, catalog):
    catalog.down = True
    response = client.post("/v1/orders", json=CART)
    assert response.status_code == 502
    assert response.json()["error"]["code"] == "catalog_unavailable"


def test_lists_a_users_orders_newest_first_and_404s_unknown_orders(client):
    first = client.post("/v1/orders", json=CART).json()
    second = client.post("/v1/orders", json=CART).json()
    client.post("/v1/orders", json={**CART, "userId": "user-2"})
    listed = client.get("/v1/orders", params={"userId": "user-1"}).json()
    assert [o["id"] for o in listed] == [second["id"], first["id"]]
    missing = client.get("/v1/orders/00000000-0000-0000-0000-000000000000")
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "unknown_order"
