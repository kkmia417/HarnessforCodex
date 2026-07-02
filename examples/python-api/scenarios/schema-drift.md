# Schema Drift Review

Use this scenario to test whether `$api-contract-review` catches contract drift
between an API schema, generated client, docs, and tests.

## Prompt

```text
Use $api-contract-review to review this API change for schema drift, client compatibility, docs, tests, and release risk.
```

## Simulated Change

A pull request changes `GET /users/{id}` to return:

```json
{
  "id": "usr_123",
  "email": "person@example.com",
  "status": "active"
}
```

The OpenAPI schema still documents `state` instead of `status`, and the Python
client fixture still asserts `state == "enabled"`.

## Expected Review

The skill should report a contract mismatch before style issues:

- API response field changed from `state` to `status`.
- OpenAPI schema and generated client fixture are stale.
- Release notes or migration notes are required if clients consume `state`.
- Tests should cover both generated client decoding and API response shape.
