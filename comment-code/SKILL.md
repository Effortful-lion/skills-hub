---
name: comment-code
description: Add, improve, or translate code comments across a project with Chinese, flow-oriented annotations. Use when Codex is asked to annotate source code, strengthen sparse comments, convert English or other-language comments to concise Chinese, add file/function/struct/interface/field/method comments, or make code easier to read without changing business logic.
---

# Comment Code

## Core Goal

Add Chinese comments that help readers follow the project flow: where data comes from, what is validated or transformed, which function/service/config is called, how errors are handled, what result is returned, and where the data goes next.

## Workflow

1. Inspect the requested scope before editing: identify target files, language conventions, existing style, AGENTS.md instructions, and whether the worktree has unrelated user changes.
2. Read enough surrounding code to understand actual behavior before writing comments; do not comment from names alone.
3. Add comments in layers: file header, exported or important types, struct fields, interface methods, functions, and then in-function flow comments.
4. Preserve business logic exactly. Do not refactor, rename, reorder, or simplify code just to add comments.
5. Translate or rewrite existing English/other-language comments into concise Chinese when they are still accurate; replace stale comments with comments that match current code.
6. Run the project’s formatter for edited files when appropriate, then review the diff to ensure only comment/formatting changes were introduced.

## Comment Style

- Write all new or rewritten comments in Chinese.
- Prefer comments that explain the role of a step in the overall flow, not only the literal syntax.
- Do not intentionally skip simple code. If a simple line is part of the request flow, configuration flow, registration flow, or data flow, add a short flow comment.
- Keep comments accurate and readable; avoid decorative comments, exaggerated wording, or comments that conflict with code.
- Use the project’s existing comment placement style where possible. For Go-style files, use `//` comments and keep file comments before `package`.

## File Header Comments

Every edited code file must have a file-level Chinese comment at the top. For files with a `package` declaration, place it before `package` and leave one blank line after the file comment.

The file header should briefly cover:

- 文件职责：该文件负责的模块、能力或业务边界。
- 核心内容：主要结构体、接口、函数、处理器、配置或注册逻辑。
- 执行流程：入口如何进入、关键步骤如何串联、结果如何输出。
- 使用场景：该文件通常由哪个模块、请求、任务或启动流程使用。
- 注意事项：特殊依赖、边界条件、临时实现、兼容逻辑或扩展点。

Example:

```go
// 文件职责：
// - 提供用户登录 HTTP 处理入口。
// - 负责解析请求参数、调用认证服务、处理认证错误并返回登录响应。
// - 通常由路由注册流程绑定到登录接口。

package handler
```

## Function Comments

Every function should have a Chinese comment immediately above it. Use this format:

```go
// FunctionName 简要说明函数的完整作用
func FunctionName(...) ...
```

The function comment should include enough context for readers to understand:

- 函数用途：该函数完成什么业务或技术能力。
- 调用场景：通常由哪个入口、服务、任务、回调或流程调用。
- 输入说明：关键参数含义、来源、约束或是否可能为空。
- 输出说明：返回值、错误、响应、状态变化或副作用。
- 流程概览：参数处理、校验、调用依赖、异常处理、结果组装、返回输出。

For very short functions, still write a concise comment that states its role in the larger flow.

## In-Function Flow Comments

Inside functions, add `//` comments before or beside meaningful steps. Prefer step comments that let a reader skim the code as a process.

Cover these common flow points when present:

- 参数入口：从请求、配置、上下文、消息、文件或数据库中取得输入。
- 参数处理：绑定、解析、转换、默认值填充、字段裁剪或格式化。
- 校验逻辑：必填检查、权限检查、状态检查、边界判断或兼容分支。
- 依赖调用：调用服务、仓储、客户端、配置中心、注册器、下游接口或工具函数，并说明调用目的。
- 结果处理：转换返回值、组装响应、写入缓存、持久化、发送消息或更新状态。
- 错误处理：说明错误来源、失败后如何返回、是否降级、是否继续执行。
- 流程出口：返回响应、返回错误、完成注册、输出配置或结束任务。

HTTP handler flow should normally be visible as:

```text
接收请求参数 -> 解析/绑定参数 -> 校验参数或权限 -> 调用业务服务 -> 处理错误 -> 组装响应 -> 返回结果
```

Non-HTTP flows should also be visible:

```text
配置管理：读取配置来源 -> 解析配置内容 -> 应用默认值 -> 校验合法性 -> 提供给业务模块
服务注册：创建实例 -> 注入依赖 -> 注册路由/处理器/服务能力 -> 暴露给调用方
数据处理：接收输入 -> 转换结构 -> 过滤/聚合/计算 -> 调用下游或持久化 -> 返回结果
```

## Structs, Fields, Interfaces

- Add a Chinese comment above every struct/type that explains its definition, purpose, business scenario, and position in the data flow.
- Add a brief Chinese comment for every struct field. Explain field meaning, purpose, source or destination, and any required/default/constraint details when relevant.
- Add a Chinese comment above every interface. Explain the capability it abstracts, main caller, implementation expectation, and how it supports decoupling or extension.
- Add a Chinese comment for every interface method. Explain method capability, important parameters, return value meaning, errors, side effects, and constraints.

## TODO Comments

Use TODO comments only for incomplete, temporary, missing, or intentionally deferred behavior. The TODO must explain both the gap and the current limitation.

Preferred format:

```go
// TODO: 补充订单状态回滚逻辑，当前仅记录错误并返回给调用方。
```

Avoid vague comments such as `// TODO` or `// 待优化`.

## Review Checklist

Before finishing, verify:

- Each edited file has a Chinese file header in the correct location.
- Each function, struct, interface, field, and interface method has an appropriate Chinese comment.
- In-function comments show the main flow, including request/config/registration/data-processing paths.
- Existing non-Chinese comments were translated or rewritten when touched.
- No business logic changed.
- Formatter output is acceptable and the final diff is limited to comments and harmless formatting.
