---
type: invariant
title: Each service owns one Postgres schema and nothing else
description: A service reads and writes only its own schema through its own login role; another service's data is reached only through that service's HTTP API.
tags: [core, data, postgres]
status: stable
generated:
  by: wmd-order-builder/gpt-5.6-terra
  at: 2026-10-04T15:45:31Z
sources:
  - id: db-connect
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/db.py#L26-L32
  - id: db-from-env
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/db.py#L61-L62
  - id: create-app
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L55-L64
  - id: reserve
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L106-L120
  - id: init-migration
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/migrations/001_init.sql#L1-L19
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/service-data-ownership.md
wardby:
  schema: 1
  roles: [builder, reviewer, planner]
  affects: [app/db.py, app/main.py, migrations/**]
  citations:
    - id: db-connect
      repo: github:chfields/wmd-order-service
      path: app/db.py
      lines: [26, 32]
      symbol: Database.connect
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:5cba58c09ef525e9d64e74e2ef57c5b2e80e13dc37bb3fe4182c757854509431
    - id: db-from-env
      repo: github:chfields/wmd-order-service
      path: app/db.py
      lines: [61, 62]
      symbol: database_from_env
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:625ff883e43c0193322b29c227fc702dcb125af8d5051054e0e37c663a434535
    - id: create-app
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [55, 64]
      symbol: create_app
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:ed72790f3392bae704e9e62805064d0dede6707a840fd83677ec4e1474cb1dfd
    - id: reserve
      repo: github:chfields/wmd-order-service
      path: app/main.py
      lines: [106, 120]
      symbol: reserve
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:2789120d4617f182b86c476cfabb4794358006f749ed7f6ab1a4cdd2c640e277
    - id: init-migration
      repo: github:chfields/wmd-order-service
      path: migrations/001_init.sql
      lines: [1, 19]
      symbol: 001_init.sql
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:4d4c15a68b06c84400bc0538a6c8cc33b62e98581b9f610bec060a23e6bd9f74
  confidence: high
---

order-service reads and writes only the `orders` schema, through a connection whose search_path is that schema. Product, price and stock data come only from catalog-service's HTTP API (POST /v1/reservations), never from a query on another schema.[^db-connect][^db-from-env][^create-app][^reserve][^init-migration]

Why: schema isolation keeps data ownership at the service boundary.

[^db-connect]: db-connect
[^db-from-env]: db-from-env
[^create-app]: create-app
[^reserve]: reserve
[^init-migration]: init-migration
