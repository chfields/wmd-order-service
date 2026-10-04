---
type: convention
title: Errors are {"error": {"code", "message"}} with stable codes
description: Every API error uses this shape, and codes are stable identifiers clients branch on, so they are never renamed.
tags: [core, api, errors]
status: stable
generated:
  by: wmd-order-builder/gpt-5.6-terra
  at: 2026-10-04T15:45:31Z
sources:
  - id: api-error
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/observability.py#L27-L34
  - id: error-handler
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/observability.py#L105-L114
  - id: reserve
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L106-L120
  - id: get-order
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L179-L185
  - id: error-tests
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/tests/test_orders.py#L45-L64
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/error-contract.md
wardby:
  schema: 1
  roles: [builder, reviewer]
  affects: [app/observability.py, app/main.py, openapi.json]
  citations:
    - id: api-error
      repo: github:chfields/wmd-order-service
      path: app/observability.py
      lines: [27, 34]
      symbol: ApiError
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:005f4b5899e02f46598e72c33ce20c28d6a89769fe9f64e8b9459347f023e610
    - id: error-handler
      repo: github:chfields/wmd-order-service
      path: app/observability.py
      lines: [105, 114]
      symbol: install._api_error
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:0a817a3256033a06bdaa1d1748e68b1d9fc3e416777a3aa54e5b27588a9db6d6
    - id: reserve
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [106, 120]
      symbol: reserve
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:2789120d4617f182b86c476cfabb4794358006f749ed7f6ab1a4cdd2c640e277
    - id: get-order
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [179, 185]
      symbol: get_order
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:3e6251db37eff2b2b3a5d9167fa3f91f9042109c3b4685d04e46edc156be285f
    - id: error-tests
      repo: github:chfields/wmd-order-service
      path: tests/test_orders.py
      lines: [45, 64]
      symbol: catalog error tests
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:848a9056edc732364e3aeabc6587fdf86d0fbd227f8922a5e41733c8ad1c4eb0
  confidence: high
---

Every error is raised as ApiError(status, code, message) and rendered as {"error": {"code", "message"}}. This service's codes (catalog_unavailable, unknown_order, plus unavailable and unknown_product passed through from catalog) are stable and must not be renamed.[^api-error][^error-handler][^reserve][^get-order][^error-tests]

What to do: preserve error codes and use ApiError for API failures.

[^api-error]: api-error
[^error-handler]: error-handler
[^reserve]: reserve
[^get-order]: get-order
[^error-tests]: error-tests
