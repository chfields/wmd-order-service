# wmd-order-service

Turns carts into orders: reserves stock with catalog-service, records the order, and confirms it once notification-service has told the customer. Part of WMD Shop, the Wardby mobile demo.

| Route | Purpose |
|---|---|
| `POST /v1/orders` | Place an order: reserve stock, record it, notify, confirm |
| `GET /v1/orders/{id}` | One order with its lines and status |
| `GET /v1/orders?userId=` | A user's orders, newest first |
| `GET /healthz`, `/readyz`, `/metrics` | Health, readiness, Prometheus metrics |

The full contract is [`openapi.json`](openapi.json). See [`AGENTS.md`](AGENTS.md)
for how to run and change it.

Orders may specify a `deliveryWindow` of `morning`, `afternoon`, or `evening`; it defaults to
`morning`.

Configuration: `DATABASE_URL` (required), `DB_SCHEMA` (default `orders`), `CATALOG_URL`, `NOTIFICATION_URL`.
