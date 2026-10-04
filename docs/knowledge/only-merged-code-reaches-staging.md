---
type: decision
title: Only merged main reaches staging
description: deploy.sh builds every service from its origin/main in a clean checkout, so staging never runs unreviewed code.
tags: [core, deploy, ci]
status: stable
generated:
  by: wmd-order-builder/gpt-5.6-terra
  at: 2026-10-04T15:45:31Z
sources:
  - id: dockerfile
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/Dockerfile#L1-L11
  - id: test-workflow
    url: https://github.com/chfields/wmd-order-service/blob/56849bc95198dcea6d3fac4e866b3dfc0156f376/.github/workflows/test.yml#L1-L28
  - id: canonical
    url: https://github.com/chfields/wmd-deploy/blob/main/docs/knowledge/core/only-merged-code-reaches-staging.md
wardby:
  schema: 1
  roles: [reviewer, planner]
  affects: [Dockerfile, .github/workflows/test.yml]
  citations:
    - id: dockerfile
      repo: github:chfields/wmd-order-service
      path: Dockerfile
      lines: [1, 11]
      symbol: Dockerfile
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:1872275d6b7dd1b4610c0cff3e812abbece7998217ba51a84e1f855cb3561c99
    - id: test-workflow
      repo: github:chfields/wmd-order-service
      path: .github/workflows/test.yml
      lines: [1, 28]
      symbol: test workflow
      sha: 56849bc95198dcea6d3fac4e866b3dfc0156f376
      spanHash: sha256:7cef579bba2a7f44dbd10a7ffedabc61710997d310718be8b13ee5536007053d
  confidence: medium
---

wmd-deploy's deploy.sh builds this repository's Dockerfile from a clean checkout of origin/main. A change reaches staging only after it is merged to main, and the test workflow gates it on every pull request.[^dockerfile][^test-workflow]

Why: the image definition packages only the checked-out application and migrations, while CI runs on pull requests and main.

[^dockerfile]: dockerfile
[^test-workflow]: test-workflow
