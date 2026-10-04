---
type: convention
title: Catalog 409/422 errors pass through to order-service callers unchanged
description: When reservation is refused, order-service re-raises catalog's status, code and message as its own, so catalog's codes are part of order-service's contract.
tags: [errors, catalog, api]
status: stable
generated:
  by: wmd-order-builder/gpt-5.6-terra
  at: 2026-10-04T15:45:31Z
sources:
  - id: reserve
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L106-L120
  - id: pass-through-test
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/tests/test_orders.py#L45-L57
  - id: outage-test
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/tests/test_orders.py#L60-L64
wardby:
  schema: 1
  roles: [builder, reviewer]
  affects: [app/main.py, openapi.json]
  citations:
    - id: reserve
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [106, 120]
      symbol: reserve
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:2789120d4617f182b86c476cfabb4794358006f749ed7f6ab1a4cdd2c640e277
    - id: pass-through-test
      repo: github:chfields/wmd-order-service
      path: tests/test_orders.py
      lines: [45, 57]
      symbol: test_passes_on_out_of_stock_and_unknown_products_creating_nothing
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:ff1253135c4f6c277260bbdf92348eeff2b652550e861695c1ffa72255f41308
    - id: outage-test
      repo: github:chfields/wmd-order-service
      path: tests/test_orders.py
      lines: [60, 64]
      symbol: test_reports_a_catalog_outage_as_502
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:e4a788073a7ff0b34d7fae31e28882e6f61f311f97572dc2150827a4586c42b4
  confidence: high
---

Catalog's codes `unavailable` (409) and `unknown_product` (422) reach order-service's callers, and through the BFF the app, unchanged. Renaming or wrapping them breaks clients, and adding a new catalog refusal status means extending this branch. Every other catalog failure is reported as 502 catalog_unavailable.[^reserve][^pass-through-test][^outage-test]

What to do: pass supported catalog refusals through exactly and map other failures to catalog_unavailable.

[^reserve]: reserve
[^pass-through-test]: pass-through-test
[^outage-test]: outage-test
