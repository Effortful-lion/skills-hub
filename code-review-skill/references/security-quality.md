# Security, Quality, And Release Reference

Use this for cross-cutting review of security, performance, tests, observability, and release readiness.

## Security

- Authentication and authorization: verify both identity and resource ownership/data scope; watch IDOR in `id`-based APIs.
- Injection: SQL, NoSQL, command, template, path traversal, SSRF, and unsafe URL redirects.
- XSS/CSRF: frontend rendering, rich text, markdown/html preview, admin consoles, cookie/session settings.
- Sensitive data: passwords, tokens, ID cards, bank cards, phone numbers, addresses, invoices, and internal IDs in logs/responses/errors.
- File handling: MIME sniffing, size limits, extension allowlist, virus scan hooks if the product requires them, storage key randomization, signed URL TTL.
- Cryptography: do not invent crypto; use project-standard hashing/signing; check nonce/timestamp replay protection for callbacks.

## Performance

- Backend: N+1 DB queries, missing indexes, full table scans, unbounded pagination, large JSON serialization, blocking RPC calls, and synchronous work in request paths.
- Cache: stampede, penetration, stale invalidation, missing TTL, overly broad cache keys, and tenant/user isolation in keys.
- Frontend: oversized bundles, unnecessary re-renders, huge table rendering, image optimization, repeated API calls, and memory leaks.
- Batch/export/import: streaming, chunking, progress, cancellation, retry, and limits for large domestic enterprise datasets.

## Tests

- Ask for tests when behavior changes. Prefer focused tests over snapshot churn.
- Go: table tests, repository/service tests, transaction rollback paths, race tests when concurrent code changes.
- Frontend: component tests for states, API mocking, form validation, route/store behavior, and e2e for critical money/order/auth flows.
- Verify bug fixes include a regression test that fails before the fix when feasible.

## Observability

- Logs should answer: who, did what, to which resource, result, latency, trace/request id.
- Metrics should exist for critical async jobs, MQ consumers, payment/callback flows, exports, and scheduled tasks.
- Alerts should trigger on repeated failure, backlog growth, dead letters, and abnormal latency/error rate.
- Avoid log spam and avoid dumping full request/response bodies by default.

## Release Risk

- Rolling deploy compatibility: old frontend with new backend, old backend with new frontend, and multiple app versions in the wild.
- Migration safety: additive first, backfill, dual-write/read if needed, then cleanup.
- Feature flags: include owner, default, rollback path, and cleanup plan.
- Config: check dev/test/prod separation, secrets manager usage, and no machine-local paths.
- Rollback: ensure new writes do not make old code unable to read critical records.
