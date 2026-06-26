# API Contract Checks

Check these surfaces together:

- route definitions
- request validation
- response schemas
- generated clients
- documentation examples
- migration notes
- compatibility tests

Flag a finding when a consumer could call the old contract and receive a
different shape, status code, error code, or required field without a documented
migration path.
