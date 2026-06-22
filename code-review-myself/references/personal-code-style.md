# 代码规范

Use these rules as the user's personal review lens. Apply them on top of the current repository's established style.

## General Stance

- First provide a refactor/review方案 when the user asks for review,规范, or方案. Do not edit code until the user explicitly asks to implement.
- Preserve behavior unless the user explicitly asks for behavior changes.
- Ensure every proposal follows the user's rules and keeps changes minimal.
- When a design is chosen, change it thoroughly instead of leaving compatibility branches or mixed old/new paths. Do not add compatibility handling unless the user explicitly asks for it.
- Respect the current project's style, naming, logging, folder layout, and framework choices.

## Code Style

1. Do not reflexively use `switch-case` to extract code. If duplicated logic is small and simple, keep direct code.
2. Do not reflexively introduce `interface`. Abstract only when there are three or more implementations with similar flow and methods and the abstraction has extension value.
3. Do not split methods only for "reuse". Extract a method only when the same semantically complete block appears in three or more places, or when extraction clearly improves a large, hard-to-follow function.
4. At key points in the call chain, especially core logic and response returns, log errors when errors occur.
5. Prefer the repository's existing log style. If no stronger local style exists, use a shape similar to: `函数接收者 | 调用的方法 | 调用的子方法 | Error | err: ...`.
6. Method names should be plain and understandable:
   - Normal processing logic: verb + noun.
   - Additional/option behavior: `with...`.
   - Query, conversion, or data-shaped logic: noun phrase.
   - Keep names creative enough to express intent, but avoid obscure cleverness.

## Engineering Structure

1. Each layer/module may have justified local differences. For example, a gateway module can have load-balancing subdirectories; modules without RPC needs can omit RPC folders.
2. Within the same project or module family, avoid inconsistent call chains such as one module using `controller -> service -> model` while another uses `controller -> logic -> service -> model` without a strong reason.
3. Keep layers shallow and responsibilities clear.
4. Do not put DTO assembly, response shaping, or similar presentation/application assembly into the model layer.
5. Model/data layers should focus on raw data query/return and error return.

## Finding Priorities

- `P1 必修`: behavior risk, broken layer responsibility, missing key error logging that affects operations, or a refactor plan likely to change semantics.
- `P2 建议修`: premature abstraction, over-split helper methods, inconsistent module layering, unclear names, DTO/model responsibility drift.
- `P3 可选`: small naming improvements or local readability issues without meaningful maintenance risk.

Do not elevate a personal style preference into a severe finding unless it creates concrete debugging, maintenance, or behavior risk.
