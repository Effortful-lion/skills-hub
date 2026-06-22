---
name: project-clone-guide
description: Use when analyzing unfamiliar codebases for project imitation, Chinese service/module/API documentation, or engineering reimplementation guidance, especially for requests such as 项目仿写, 通读项目, 生成模块文档, 生成接口文档, 梳理服务功能, or 分析陌生项目.
---

# Project Clone Guide

## Goal

Generate a code-evidence-based project imitation guide for an unfamiliar codebase. Convert implementation structure into business-facing service, module, and API documentation that helps the user reimplement a similar project without copying code blindly.

Write output in Chinese unless the user asks for another language. Generate documentation under `guide-docs/` in the analyzed project's root directory unless the user specifies another output path.

## First Pass

Start by building a project map before writing documentation:

1. Identify language, framework, build files, service entrypoints, configuration files, route registration, middleware, response helpers, error/status code definitions, models, repositories, external integrations, code generation tools, and framework-specific workflow artifacts such as `.api`, `proto`, schema, or model definitions.
2. Use `rg`, `rg --files`, framework route commands, generated OpenAPI files, or existing docs when available. Prefer code evidence over naming guesses.
3. Trace each public route from router/controller/handler to service/domain logic, data access, external calls, and response construction.
4. Infer the project's engineering workflow from code structure and toolchain: note whether the framework expects model-first, schema-first, contract-first, codegen-first, or hand-written development, and identify the real build order that a reimplementation should follow.
5. Prepare a concise file overview for the root project overview: list important directories and files with one short description of what each contains or why it matters to reimplementation.
6. Record uncertain items as "未在代码中确认" instead of inventing details.

## Service And Module Discovery

Group findings by business service first, then by functional module:

- Treat independently deployed apps, route groups, bounded domains, or top-level packages as candidate services.
- Treat cohesive business capabilities as modules, even when the code is split across handler/service/repository files.
- If service boundaries are unclear, create a single `project-service/` folder and explain the inferred boundaries in `overview.md`.
- Use stable lowercase snake-case filenames, such as `user_info.md` and `user_info_api.md`.

Recommended output tree:

```text
guide-docs/
├── overview.md
├── user-service/
│   ├── overview.md
│   ├── user_info.md
│   └── user_info_api.md
└── file-service/
    ├── overview.md
    ├── attachment_upload.md
    └── attachment_upload_api.md
```

## Documentation Workflow

At the root of `guide-docs/`:

1. Create `overview.md` from `references/project-overview-template.md`.
2. Use this file only for project positioning, directory/file overview, service/module map, technology stack identification, framework-specific development workflow guidance, and an engineering-grounded reimplementation route.
3. Order the route by real engineering dependencies and core business value: foundational dependencies first, core modules early, dependent or peripheral modules later.
4. If the framework or toolchain implies a preferred implementation sequence, make that sequence explicit. Examples include model/schema definitions before generators, contract files before generated handlers, or initialization/bootstrap code before business logic wiring.
5. Do not frame the route as copying code file-by-file.

For the root overview's file overview:

- List important source directories and key files, not every generated or vendor file.
- Add one concise factual description for each directory/file.
- Explain why each item matters to understanding, reimplementing, or extending the project.
- Mark inferred descriptions as "根据代码结构推断" when the purpose is not directly documented.

For each service:

1. Create `overview.md` from `references/service-overview-template.md`.
2. Create one `{module}.md` per functional module from `references/module-template.md`.
3. Create one `{module}_api.md` per module that exposes HTTP/RPC endpoints from `references/api-template.md`.
4. Include source evidence for important conclusions with file paths and, when useful, line numbers.

For each API:

- Extract route, method, path/query/body/header parameters, auth requirements, response fields, status codes, and examples from code.
- Every documented interface must include its own complete request example and complete response example. Do not replace per-interface examples with a shared or generic example.
- Request examples must include method, full route with path/query parameters, required headers, content type, and a realistic body/form payload when the interface accepts one. Omit body payload only when the method and code path truly do not accept a body.
- Response examples must include the complete response envelope and representative `body` fields confirmed from code. Mark uncertain fields as "未在代码中确认" in prose, not inside invalid JSON.
- Distinguish HTTP status codes from business status codes. If the code uses a sub-code helper such as `WithSubCode`, document the business status code.
- If examples require hostnames or tokens that are not present, use placeholder values such as `https://example.com` and `<TOKEN>`.
- Keep curl examples runnable after replacing placeholders.

## Quality Bar

Produce documents that answer:

- What business capability does this module provide?
- Which interfaces expose the capability?
- What is the core business flow?
- Which data structures, storage tables, caches, queues, files, or external services are involved?
- What tech stack, framework, and code generation tools shape the reimplementation path, and what development sequence do they imply?
- What are the key technical design points worth preserving when reimplementing?
- Which parts are confirmed by code, and which parts remain uncertain?
- What is the recommended engineering order for reimplementing a similar project?

Avoid copying large code blocks. Summarize behavior and cite the relevant source files.

## References

- Use `references/project-overview-template.md` for the root `guide-docs/overview.md`.
- Use `references/service-overview-template.md` for service folders.
- Use `references/module-template.md` for module explanation files.
- Use `references/api-template.md` for interface documentation files.
