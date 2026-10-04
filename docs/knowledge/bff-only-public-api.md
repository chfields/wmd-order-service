---
type: invariant
title: The BFF is the only API the app and the outside world reach
description: wmd-app calls only wmd-bff; services stay internal and trust the user id the BFF passes, never one taken from a request body.
tags: [core, security, api]
status: stable
generated:
  by: wmd-order-builder/gpt-5.6-terra
  at: 2026-10-04T15:45:31Z
sources:
  - id: order-request
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L29-L31
  - id: place
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L145-L177
  - id: list-for-user
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L187-L196
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/bff-only-public-api.md
wardby:
  schema: 1
  roles: [builder, reviewer, planner]
  affects: [app/main.py, openapi.json]
  citations:
    - id: order-request
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [29, 31]
      symbol: OrderRequest.userId
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:341b3cb4d01ec48a5097f38db6661e2652037e01fc5bf7335a61427106dd0e78
    - id: place
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [145, 177]
      symbol: place
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:1de4fb834477724c0311e8afcaf2ddece8377dfad9bf95ac9785e08928997201
    - id: list-for-user
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [187, 196]
      symbol: list_for_user
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:17973af3643a2f3a5f819a26df1b1956bfe1c72583138b98e80e382bba1652f8
  confidence: medium
---

order-service does no authentication. It trusts the userId in POST /v1/orders and GET /v1/orders?userId= because only wmd-bff calls it, and the BFF fills that id from the authenticated user, never from what the app sent. So the service must never be exposed publicly, and nothing in it should treat the userId as proof of identity from any other caller.[^order-request][^place][^list-for-user]

What to do: keep this service internal and treat userId as BFF-supplied context.

[^order-request]: order-request
[^place]: place
[^list-for-user]: list-for-user
