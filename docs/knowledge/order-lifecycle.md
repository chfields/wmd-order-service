---
type: invariant
title: Orders reserve stock first and are confirmed only after notification
description: An order exists only after catalog-service reserves all its stock in one transaction, and moves from pending to confirmed only when notification-service accepts the confirmation, which is idempotent per order and kind.
tags: [core, orders, domain]
status: stable
generated:
  by: wmd-order-builder/gpt-5.6-terra
  at: 2026-10-04T15:45:31Z
sources:
  - id: place
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L145-L177
  - id: reserve
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L106-L120
  - id: notify
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L122-L143
  - id: init-migration
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/migrations/001_init.sql#L1-L19
  - id: lifecycle-tests
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/tests/test_orders.py#L12-L57
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/order-lifecycle.md
wardby:
  schema: 1
  roles: [builder, reviewer, planner]
  affects: [app/main.py, migrations/**]
  citations:
    - id: place
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [145, 177]
      symbol: place
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:1de4fb834477724c0311e8afcaf2ddece8377dfad9bf95ac9785e08928997201
    - id: reserve
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [106, 120]
      symbol: reserve
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:2789120d4617f182b86c476cfabb4794358006f749ed7f6ab1a4cdd2c640e277
    - id: notify
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [122, 143]
      symbol: notify
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:afe2622eb252c4e01dafeabf7197906d1762a43151fb09b8cdc21a819a43a295
    - id: init-migration
      repo: github:chfields/wmd-order-service
      path: migrations/001_init.sql
      lines: [1, 19]
      symbol: 001_init.sql
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:4d4c15a68b06c84400bc0538a6c8cc33b62e98581b9f610bec060a23e6bd9f74
    - id: lifecycle-tests
      repo: github:chfields/wmd-order-service
      path: tests/test_orders.py
      lines: [12, 57]
      symbol: order lifecycle tests
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:289ba756794882bb7bf7ca8e558c6fc2c1135d58817cb3b97b0aa5e1206d69d7
  confidence: high
---

`place` calls catalog's POST /v1/reservations before it writes any row, so a refused reservation creates no order. The order is inserted as pending and becomes confirmed only if notification-service answers 200/201 to {orderId, kind: "order_confirmed", deliveryWindow}; an optional gift message is included with that confirmation. A failed notification leaves the order pending, and the call still returns 201.[^place][^reserve][^notify][^init-migration][^lifecycle-tests]

Why: stock reservation precedes persistence, while notification acceptance controls confirmation.

[^place]: place
[^reserve]: reserve
[^notify]: notify
[^init-migration]: init-migration
[^lifecycle-tests]: lifecycle-tests
