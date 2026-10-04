---
type: invariant
title: The order id is minted before reservation and used as catalog's orderRef
description: place() generates the order uuid, reserves stock under that orderRef, and only then inserts the order; the order's total and line names and prices come from the reservation response, not from the request.
tags: [orders, catalog, domain]
status: stable
generated:
  by: wmd-order-builder/gpt-5.6-terra
  at: 2026-10-04T15:45:31Z
sources:
  - id: place
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L145-L177
  - id: reserve
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L106-L120
  - id: order-ref-test
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/tests/test_orders.py#L12-L29
wardby:
  schema: 1
  roles: [builder, reviewer]
  affects: [app/main.py]
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
    - id: order-ref-test
      repo: github:chfields/wmd-order-service
      path: tests/test_orders.py
      lines: [12, 29]
      symbol: test_places_an_order_and_confirms_it_once_the_customer_is_notified
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:a0385590087d1eb4463e33f1faa0a9dae566d6c51c2907180e9e6e3bc1ba0781
  confidence: high
---

The order uuid exists before any row does and is sent as orderRef, which ties catalog's reservation to the order. Prices, names and the total are copied from catalog's reservation response, so never compute them from the request. If the insert fails after a successful reservation, the stock stays reserved and nothing compensates, so keep the code between reserve and insert minimal.[^place][^reserve][^order-ref-test]

What to do: mint and reserve with the order id before persistence, and trust reservation pricing.

[^place]: place
[^reserve]: reserve
[^order-ref-test]: order-ref-test
