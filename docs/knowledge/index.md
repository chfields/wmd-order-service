# Architecture knowledge

## Core

- [Each service owns one Postgres schema and nothing else](service-data-ownership.md)
- [The BFF is the only API the app and the outside world reach](bff-only-public-api.md)
- [Every request carries one x-correlation-id end to end](correlation-id-propagation.md)
- [Errors are {"error": {"code", "message"}} with stable codes](error-contract.md)
- [Orders reserve stock first and are confirmed only after notification](order-lifecycle.md)
- [Only merged main reaches staging](only-merged-code-reaches-staging.md)

## This repository

- [Catalog 409/422 errors pass through to order-service callers unchanged](catalog-errors-pass-through.md)
- [The order id is minted before reservation and used as catalog's orderRef](reservation-before-order-row.md)
