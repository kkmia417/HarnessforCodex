---
name: api-contract-review
description: Review Python API contract changes, schemas, generated clients, documentation, tests, and release compatibility. Use when asked to check API changes, schema drift, OpenAPI updates, client compatibility, or integration release risk.
---

# API Contract Review

Review API changes as a compatibility contract, not only as code.

## Workflow

1. Identify changed routes, schemas, request models, response models, and generated clients.
2. Compare documented behavior with implementation behavior.
3. Check backward compatibility for existing consumers.
4. Verify tests cover new and changed contracts.
5. Summarize release risk and required migration notes.

Read `references/api-contract-checks.md` before producing findings.
