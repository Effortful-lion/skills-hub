---
name: deploy-review
description: "Review a current project and decide whether it is ready for the simplest safe launch as a solo-developer product. Use when Codex needs to inspect an existing codebase or product repo and answer: what already exists, what is still missing before launch, which scripts or release steps are actually necessary, and which processes should not be added yet in order to keep operations lightweight."
---

# Deploy Review

Review the current project as a solo developer preparing to launch. Optimize for the smallest safe operational surface, not process completeness.

## Core stance

- Assume the user wants the lightest viable release process.
- Recommend additional scripts, checks, or workflows only when they reduce real launch risk.
- Prefer a missing but critical safety mechanism over a polished but optional process.
- Avoid importing team-scale rituals into solo projects unless the project complexity clearly justifies them.

## Analyze the project

1. Inspect the repository and deployment context before giving advice.
2. If the repo root contains `.codegraph/`, use CodeGraph before grep or broad file reads to understand entrypoints, deployment scripts, and release paths.
3. Look for concrete launch signals such as:
   - run or build scripts
   - environment configuration
   - deployment manifests or infra config
   - database migration or seed flow
   - rollback path
   - backup or data export path
   - logging, alerting, or health checks
   - release notes, changelog, or manual release steps
   - CI or automation that already reduces operational work
4. Distinguish between what exists in code, what exists only as tribal knowledge, and what is completely missing.
5. Judge the project by current complexity, not by an idealized future architecture.

Read [references/complexity-guide.md](references/complexity-guide.md) when you need the complexity ladder or default recommendation thresholds.

## Recommendation rules

- For simple static sites, small tools, single-binary apps, or low-risk internal utilities, favor manual release steps plus 1-2 critical scripts over CI/CD sprawl.
- For products with stateful data, background jobs, payments, user accounts, or non-trivial infra, raise the bar for rollback, backups, migrations, and observability.
- If a task can be handled by one repeatable script, recommend the script instead of a new process document.
- If a process exists but increases cognitive load without reducing meaningful risk, say not to add it yet.
- If information is missing, say so explicitly instead of pretending the repo proves more than it does.

## Output contract

Do not create a file unless the user explicitly asks you to write one.

Default to returning a minimal document in chat with this exact structure:

```markdown
# 发布检查清单
- [ ] ...
- [ ] ...

## 现在有什么
- ...

## 还缺什么
- ...

## 暂时不建议增加什么
- ...
```

## Checklist rules

- Put the most launch-critical checks first.
- Keep the checklist short; prefer 5-10 items.
- Phrase each item as something the user can verify before release.
- Include only checks that matter for this project's actual risk level.

## Section rules

### 现在有什么

- List only concrete capabilities, scripts, or workflows that were actually found.
- Prefer terse statements tied to evidence in the repo.

### 还缺什么

- List only gaps that materially affect launch safety, maintainability, or recovery.
- For each gap, recommend the smallest viable next step.
- Mention scripts when a script is the cleanest fix.

### 暂时不建议增加什么

- Explicitly name processes that might sound professional but are not justified yet.
- Explain briefly why skipping them now lowers cognitive or ops complexity.

## Tone

- Be direct, calm, and low-ceremony.
- Sound like an experienced solo builder protecting future maintenance burden.
- Prefer "enough to ship safely" over "best practice says".
