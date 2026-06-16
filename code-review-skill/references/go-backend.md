# Go Backend Review Reference

Use this for Go services, HTTP/RPC handlers, jobs, repositories, middleware, migrations, and shared packages.

## Must-Check Areas

- Error handling: never ignore `err`; wrap with `%w` at boundaries; use `errors.Is/As`; avoid logging and returning the same error repeatedly.
- Context: pass `context.Context` from entrypoints to DB/RPC/cache/MQ calls; respect cancellation/timeouts; do not store context in structs.
- Concurrency: every goroutine needs an exit path; protect shared state; avoid unbounded worker creation; run `go test -race` when races are plausible.
- API compatibility: preserve JSON/protobuf field names, status codes, error codes, pagination contracts, and nullable/zero-value semantics.
- Transactions: keep transaction scope explicit; rollback on every failure path; avoid external RPC/MQ calls inside long DB transactions.
- Idempotency: callbacks, jobs, retries, MQ consumers, payment/order flows, and batch imports must tolerate duplicate execution.
- Observability: log request id/trace id and business ids; avoid noisy logs in loops; never log passwords, tokens, ID cards, phone numbers, or full payloads with secrets.
- Tests: add table tests for edge cases; mock at external boundaries; include repository/service tests for transaction/idempotency logic.

## Go Style And Design

- Keep interfaces small and consumer-owned. Do not create `IUserService`-style interfaces only because Java/Spring habits suggest it.
- Return concrete types from constructors and accept interfaces at call sites when needed.
- Use pointer receivers when methods mutate state, contain mutexes, or copying is expensive. Keep receiver choice consistent.
- Avoid package names like `common`, `utils`, and `base` when a domain name is possible.
- Prefer `time.Time` and explicit timezone handling over strings. Review `Asia/Shanghai` assumptions in reports, settlement, and daily jobs.
- Avoid global mutable state except initialized configuration/clients with clear lifecycle.
- Do not panic in request paths except truly unrecoverable programmer errors. Convert domain failures into typed errors or standard response codes.

## HTTP And Service Layers

- Validate all external input at the boundary: path/query/body/header, file metadata, enum values, and pagination limits.
- Keep handlers thin: parse, authorize, call service, map response. Put business invariants in services, not only controllers.
- Check auth and data scope before loading or mutating sensitive resources. Do not rely on frontend-hid buttons.
- Use consistent response envelopes and error codes used by the project. Avoid mixing English-only messages into a Chinese product unless the project does.
- For uploads/downloads, check content type, size, extension, storage path traversal, signed URL expiry, and authorization.

## Database, Cache, MQ

- MySQL: check indexes for new query paths; avoid N+1 queries; verify `WHERE tenant_id/user_id/status/deleted_at` filters; use optimistic locks/version fields when needed.
- GORM/sqlx/sqlc: check zero-value update behavior, `RowsAffected`, `Preload` fanout, raw SQL injection, and missing `Limit`.
- Redis: set TTL where appropriate; avoid cache penetration; review lock expiration and unlock ownership tokens.
- MQ/jobs: ensure ack/nack semantics, retry strategy, dead-letter handling, idempotent consumer keys, and alertable failures.
- Migrations: make them backward compatible for rolling deploys; split schema and code if needed; avoid blocking full-table operations during peak hours.

## Common Findings

- `defer` inside large loops causing delayed release of files/rows/locks.
- `time.Now()` scattered through business code, making tests flaky and timezone behavior implicit.
- Shadowed `err` inside transactions causing commit after a failed operation.
- Missing `Close()` for `rows`, response bodies, files, tickers, or clients.
- Treating `sql.ErrNoRows` as system error instead of domain not-found.
- Goroutine captures loop variables or writes shared maps/slices without protection.
- JSON `omitempty` accidentally changes API semantics for mobile clients.
- Hardcoded internal domains, app ids, OSS bucket names, or feature switches.
