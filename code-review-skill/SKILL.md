---
name: code-review-skill
description: 项目代码审查, the Chinese-facing name for code-review-skill. Chinese-oriented code review workflow for Go backend services and Vue/React/Flutter frontends. Use when reviewing local diffs, PR/MR changes, staged changes, commits, or code snippets for correctness, security, performance, maintainability, tests, Go engineering practice, and domestic China team conventions such as clear Chinese feedback, interface compatibility, log/trace conventions, MySQL/Redis/MQ usage, config hygiene, and release risk.
---

# 项目代码审查

Use this skill as `code-review-skill` internally and present it to users as `项目代码审查`. Produce focused, actionable Chinese code reviews for Go backend and frontend changes. Prioritize real defects and merge risk over style taste.

## Review Workflow

1. Identify the review target: local diff, staged diff, commit range, PR/MR, or pasted snippet.
2. Gather context before judging: read the requirement, changed files, nearby call sites, tests, configuration, migrations, routes, and generated/API contracts.
3. Select references only as needed:
   - Go backend: read [references/go-backend.md](references/go-backend.md).
   - Vue/React/Flutter frontend: read [references/frontend.md](references/frontend.md).
   - Cross-cutting security, performance, tests, and release risk: read [references/security-quality.md](references/security-quality.md).
4. Run cheap verification when local context allows: `git diff`, `go test ./...`, targeted frontend tests/builds, linters, or type checks. If verification is too expensive or unavailable, say exactly what was not run.
5. Report findings first, ordered by severity. Include exact file/line references, why it matters, and a concrete fix direction.

## Severity

- `P0 阻断`: data loss, auth bypass, payment/order/account risk, irreversible migration risk, production outage, secret leakage.
- `P1 必修`: correctness bug, race/leak, broken API compatibility, security gap, serious performance regression, missing transaction/rollback.
- `P2 建议修`: maintainability, test gap, edge case, observability, inconsistent contract, moderate performance concern.
- `P3 可选`: naming, local readability, minor cleanup. Do not lead with P3 unless no higher-risk issue exists.

## Domestic Team Biases

Check the things that often break in China-based product teams:

- API compatibility with app/web clients, mini-programs, admin systems, OpenAPI/Swagger docs, and backward-compatible JSON field names.
- Permission boundaries: RBAC/data-scope/tenant isolation, admin-only APIs, IDOR, export/download authorization.
- MySQL transaction boundaries, idempotency for payment/order/callback/job handlers, and Redis/MQ consistency.
- Log and trace usefulness: `trace_id`/`request_id`, business identifiers, no secrets/PII, Chinese operational context when useful.
- Config hygiene: no hardcoded internal domains, tokens, bucket names, feature switches, or environment-specific values in code.
- Release safety: migration order, gray release switches, rollback behavior, cache invalidation, cron/job duplication.

## Output Contract

Use Chinese by default. Be direct, specific, and respectful.

Start with one of:

- `发现 N 个问题`
- `未发现阻断问题`
- `无法完整确认，原因是...`

For each finding, use:

```markdown
- [P1 必修] 标题
  文件: /abs/path/to/file.go:123
  问题: 说明当前代码在什么条件下会失败。
  影响: 说明线上或用户影响。
  建议: 给出可执行修复方向，必要时附简短代码片段。
  [💬]comment：可直接复制到 PR/MR 行内评论的简短中文评论。

- [P2 建议修] 下一个标题
  文件: /abs/path/to/file.ts:45
  问题: 说明问题。
  影响: 说明影响。
  建议: 说明建议。
  [💬]comment：可直接复制到 PR/MR 行内评论的简短中文评论。
```

Keep exactly one blank line between adjacent findings. Put the `[💬]comment：` line immediately after the `建议:` line inside every finding.

Then add:

- `验证`: commands run and results, or why not run.
- `剩余风险`: only include if relevant.

Avoid long praise sections. Mention good parts briefly only after findings.

## Review Discipline

- Prefer evidence over assumptions. If a concern depends on unknown business rules, mark it as a question instead of a defect.
- Do not request broad rewrites unless the current design creates concrete risk.
- Do not manually nitpick formatting that `gofmt`, ESLint, Prettier, Dart format, or CI can enforce.
- When reviewing generated files, migrations, protobuf/OpenAPI, or lockfiles, focus on compatibility and drift.
- If the user asks to fix findings, change only the relevant files and re-run targeted verification.
