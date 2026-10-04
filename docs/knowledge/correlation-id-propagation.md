---
type: convention
title: Every request carries one x-correlation-id end to end
description: Each service accepts x-correlation-id (or makes one), logs it, returns it, and forwards it on every outbound call.
tags: [core, observability, logging]
status: stable
generated:
  by: wmd-order-builder/gpt-5.6-terra
  at: 2026-10-04T15:45:31Z
sources:
  - id: correlation-header
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/observability.py#L19-L23
  - id: json-formatter
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/observability.py#L42-L53
  - id: observability-dispatch
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/observability.py#L66-L102
  - id: reserve
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L106-L120
  - id: notify
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/app/main.py#L122-L143
  - id: forwarding-test
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/tests/test_orders.py#L32-L35
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/correlation-id-propagation.md
wardby:
  schema: 1
  roles: [builder, reviewer]
  affects: [app/observability.py, app/main.py]
  citations:
    - id: correlation-header
      repo: github:chfields/wmd-order-service
      path: app/observability.py
      lines: [19, 23]
      symbol: CORRELATION_HEADER
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:26cd296ad0453cbb92a5bfa2737234b9534685c378535426e4eb4c709c6b92de
    - id: json-formatter
      repo: github:chfields/wmd-order-service
      path: app/observability.py
      lines: [42, 53]
      symbol: JsonFormatter.format
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:051ae050296ed2d90b16fc3a0ba5a493d324e69f3b0df77d2b4f2a22794f96af
    - id: observability-dispatch
      repo: github:chfields/wmd-order-service
      path: app/observability.py
      lines: [66, 102]
      symbol: _Observability.dispatch and outbound_headers
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:817cf06c2cabc8e1098f6c023e34a47d30b540e5e986280b04489a38922f664d
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
    - id: forwarding-test
      repo: github:chfields/wmd-order-service
      path: tests/test_orders.py
      lines: [32, 35]
      symbol: test_forwards_the_correlation_id_to_both_services
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:8d99156f98d4a3ca5d543a7b1cc26501f9f58c53229ce57897cef923835112bb
  confidence: high
---

The middleware accepts x-correlation-id if it matches ^[A-Za-z0-9._-]{1,128}$ and otherwise makes a uuid4. It stores the id in a contextvar, logs it on every JSON line, and returns it in the response header. Every outbound httpx call must pass headers=outbound_headers().[^correlation-header][^json-formatter][^observability-dispatch][^reserve][^notify][^forwarding-test]

What to do: propagate the current correlation id on every new outbound call.

[^correlation-header]: correlation-header
[^json-formatter]: json-formatter
[^observability-dispatch]: observability-dispatch
[^reserve]: reserve
[^notify]: notify
[^forwarding-test]: forwarding-test
