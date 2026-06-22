---
name: code-review-myself
description: >-
  代码规范助手. Use when the user asks for code review, project refactor review, review方案, 重构方案, 按我的代码规范, 个人开发习惯, or style-focused review for local diffs, PR/MR changes, commits, snippets, and Go/backend project code. Focus on the user's personal engineering style: conservative abstraction, minimal but thorough changes, no compatibility layering when changing, clear layering, model purity, logging at key error paths, and scheme-first review before code edits unless explicitly authorized.
---

# 代码规范助手

Use this skill to review code and produce refactor plans according to the user's personal coding standards. Default to Chinese output.

## Core Workflow

1. Identify the review target: local diff, staged diff, commit range, PR/MR, specific files, or pasted code.
2. Gather only necessary context: changed files, nearby call sites, routing/handler entry points, service/model boundaries, tests, logs, and existing project style.
3. Read [references/personal-code-style.md](references/personal-code-style.md) before judging style, refactor shape, layering, logging, or naming.
4. Review in this order: correctness and behavior preservation, project layering, abstraction restraint, logging/error handling, naming, and test/verification risk.
5. If the user asks for review or refactor guidance, provide a方案 first and do not edit code.
6. Edit code only when the user explicitly asks to implement/fix/refactor. Keep changes minimal in scope but thorough in the chosen direction.
7. Run relevant verification when possible; if not run, state the exact reason.

## Review Biases

- Prefer direct, readable code over premature switch-case extraction, interfaces, or tiny helper methods.
- Introduce abstraction only when it is justified by at least three similar implementations with similar flow and methods, and the abstraction has real extensibility value.
- Keep architecture layers shallow and consistent inside the same project/module family.
- Keep DTO assembly and response shaping out of model/data access layers.
- When changing a design, avoid adding compatibility branches or dual paths unless the user explicitly asks for compatibility.

## Output Contract

For a review/refactor request, use:

```markdown
### 评审结论
简短说明是否建议调整，以及最大风险点。

### 问题清单
- [P1/P2/P3] 标题
  文件: /abs/path/file.go:123
  问题: 具体违反了什么规范或会造成什么维护/行为风险。
  建议: 给出可执行修改方向。

### 重构方案
1. 按执行顺序列出最小必要步骤。
2. 说明哪些地方保持不动，避免过度改造。

### 验证建议
列出应运行的测试、构建或手工验证点。
```

For implementation requests, first restate the accepted plan briefly, then change only relevant files and report verification.
