---
name: comment-code
description: Add, improve, or translate code comments across a project with concise Chinese, flow-oriented annotations. Use when Codex is asked to annotate source code, strengthen sparse comments, convert English or other-language comments to Chinese, add file/function/struct/interface/message/proto/field/method comments, or make code easier to read without changing business logic.
---

# Comment Code

## Core Goal

Add concise Chinese comments that make code easier to follow: what the file owns, what each type represents, where inputs come from, what is validated or transformed, which dependency is called, how errors are handled, what is returned, and where data goes next.

## Workflow

1. Inspect the requested scope first: target files, language conventions, existing comment style, AGENTS.md instructions, generated-code markers, and unrelated user changes.
2. Read enough surrounding code to understand real behavior; do not infer comments from names alone.
3. Add comments in layers: file header, types/messages/interfaces, fields/methods, functions, then key in-function flow steps.
4. Preserve business logic exactly. Do not refactor, rename, reorder, simplify, or alter generated code.
5. Translate or rewrite touched English/other-language comments into concise Chinese when still accurate; replace stale comments with accurate ones.
6. Do not run project code, tests, builds, services, scripts, generators, or formatters while performing comment-only work.
7. Review the diff to ensure changes are limited to comments only. Revert any accidental non-comment edits before finishing.

## Hard Boundaries

- Only add, improve, or translate comments. Do not change executable code, declarations, imports, formatting-only whitespace, generated output, configuration values, tests, scripts, or project behavior.
- Do not run the project, invoke test/build/lint/format commands, start services, execute scripts, regenerate files, or call tools that modify code automatically.
- Use reading and diff inspection to verify the work. If validation would require execution, state that it was intentionally skipped because this skill is comment-only.

## Generated Code

- Do not edit files or blocks marked as generated, auto-created, vendor-owned, or "do not modify".
- Treat common generated markers as hard stops, including `Code generated`, `DO NOT EDIT`, `@generated`, generated protobuf/grpc files, generated OpenAPI clients, and tool output headers.
- If the whole file is generated, leave it unchanged and mention that it was skipped.
- If only part of a file is generated, comment only the human-owned section and keep generated blocks untouched.

## Comment Style

- Write all new or rewritten comments in Chinese.
- Keep comments short, specific, and useful. Prefer one clear sentence over a broad paragraph.
- Explain the role in the flow, not the obvious syntax.
- Do not skip simple code when it participates in request handling, configuration, registration, messaging, persistence, or data transformation.
- Avoid decorative comments, vague praise, duplicated wording, and comments that conflict with code.
- Follow the file's existing placement style. For Go files, use `//` comments and keep the file comment before `package`.

### SQL and Config Files

- For SQL files, use block comments such as `/* ... */` for the file-level overview, and use line comments such as `--` for field-level notes on complex table structures when needed.
- For YAML, TOML, INI, and similar config files, use the comment syntax supported by the file format to add a brief file-level description and concise notes for individual settings, including nested or multi-level settings.
- When the configuration meaning is tightly coupled to the project and cannot be confirmed from surrounding context, related code, or existing conventions, do not invent business meaning; keep the comment generic or skip it.

## File Header Comments

Every edited non-generated code file must have a concise Chinese file-level comment at the top. For files with a `package` declaration, place it before `package` and leave one blank line after the file comment.

Make the file explanation concrete and brief. Cover only what exists in the file:

- 文件职责：该文件负责的模块、业务边界或技术能力。
- 核心内容：主要结构体、接口、message、处理器、配置、注册逻辑或工具函数。
- 流程位置：入口从哪里来，关键步骤如何串联，结果给谁使用。
- 使用场景：通常由哪个请求、任务、启动流程、消息消费或业务模块调用。
- 注意事项：真实存在的依赖、边界条件、兼容逻辑、扩展点或生成代码跳过原因。

Example:

```go
// 文件职责：
// - 承接登录接口的 HTTP 请求，完成参数解析、认证调用和响应返回。
// - 主要包含登录处理器和请求/响应结构，供路由注册后被客户端请求触发。
// - 失败时将认证错误转换为接口错误，成功时返回登录态信息。

package handler
```

## Types, Messages, Interfaces

Add a short Chinese explanation for every human-owned declaration that defines data or behavior:

- `struct` / `class` / `type` / `record` / `data class`: explain what it represents, main scenario, and its position in input, persistence, business processing, or output.
- `interface` / `protocol` / abstract type: explain the capability it abstracts, main caller, expected implementation, and extension boundary.
- `message` / protobuf message / request / response / event / command / DTO / VO / entity / model: explain the data meaning, producer, consumer, and whether it is used for request input, response output, storage, or message delivery.
- `enum` / const group: explain the state or category set, where values are produced, and where they affect branching.
- Interface or message methods must explain their capability, important parameters, return value, errors, side effects, and constraints when present.

Keep these comments compact. One useful line is enough for simple declarations.

## Fields

Add a brief Chinese comment for every human-owned field in structs, messages, config objects, request/response objects, and persisted models.

Each field comment should state:

- 字段含义：这个字段代表什么。
- 流向：来自请求、配置、数据库、消息、下游接口，还是返回给调用方。
- 约束：必填、默认值、单位、枚举、范围、兼容含义或为空语义。

Skip fields only when they belong to generated or unmodifiable code.

## Function Comments

Every human-owned function or method should have a Chinese comment immediately above it. Use this shape when the language supports it:

```go
// FunctionName 说明函数在当前流程中的完整作用。
func FunctionName(...) ...
```

Include the important context, but stay concise:

- 用途：完成什么业务或技术能力。
- 调用场景：由哪个入口、服务、任务、回调或流程调用。
- 输入：关键参数来源、约束、是否可空。
- 输出：返回值、错误、响应、状态变化或副作用。
- 流程：校验、依赖调用、异常处理、结果组装和返回。

For very short functions, still add one concise comment that places it in the larger flow.

## In-Function Flow Comments

Inside functions, add `//` comments before or beside meaningful steps so a reader can skim the process.

Cover these flow points when present:

- 参数入口：从请求、配置、上下文、消息、文件或数据库取得输入。
- 参数处理：绑定、解析、转换、默认值填充、字段裁剪或格式化。
- 校验逻辑：必填、权限、状态、边界、幂等或兼容判断。
- 依赖调用：调用服务、仓储、客户端、配置中心、注册器、下游接口或工具函数，并说明目的。
- 结果处理：转换返回值、组装响应、写入缓存、持久化、发送消息或更新状态。
- 错误处理：说明错误来源、失败返回、降级、重试或继续执行策略。
- 流程出口：返回响应、返回错误、完成注册、输出配置或结束任务。

Common flows:

```text
HTTP：接收请求 -> 绑定参数 -> 校验参数/权限 -> 调用服务 -> 处理错误 -> 组装响应 -> 返回结果
配置：读取来源 -> 解析内容 -> 应用默认值 -> 校验合法性 -> 提供给业务模块
注册：创建实例 -> 注入依赖 -> 注册路由/处理器/服务能力 -> 暴露给调用方
数据：接收输入 -> 转换结构 -> 过滤/聚合/计算 -> 调用下游或持久化 -> 返回结果
消息：接收消息 -> 解析载荷 -> 校验幂等/状态 -> 调用业务 -> 确认、重试或丢弃
```

## TODO Comments

Use TODO comments only for incomplete, temporary, missing, or intentionally deferred behavior. The TODO must explain both the gap and the current limitation.

Preferred format:

```go
// TODO: 补充订单状态回滚逻辑，当前仅记录错误并返回给调用方。
```

Avoid vague comments such as `// TODO` or `// 待优化`.

## Review Checklist

Before finishing, verify:

- Each edited non-generated file has a concrete, concise Chinese file header in the correct location.
- Generated or unmodifiable files/blocks were not changed.
- Every human-owned function, method, struct, type, interface, message, request/response object, DTO/model/entity, enum, field, and interface/message method has a useful Chinese comment.
- In-function comments show the main request, config, registration, data-processing, persistence, or messaging flow.
- Existing non-Chinese comments were translated or rewritten when touched.
- No business logic changed.
- No code, formatting-only whitespace, generated output, config value, test, script, or behavior change was introduced.
- No project code, tests, builds, services, scripts, generators, linters, or formatters were run.
