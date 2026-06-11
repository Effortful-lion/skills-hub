---
name: yuni-api-docs
description: 从 Yuni/Codis Go 项目的 ims 路由与 handler 代码生成中文 Markdown API 文档。适用于用户要求“生成接口文档”“根据代码批量整理 API 文档”“为 HTTP 或 cmd 接口各生成一个 md”“扫描 ims.HttpRSETRouter、ims.HttpRouterNoVerify、ims.HttpRESTRouterNoVerify、ims.WithImjHandler、ims.WithImjHandlerNoVerify 并推导参数、状态码、curl 示例、ImjCommand 响应结构”的场景。
---

# Yuni API Docs

## Overview

使用该 skill 生成或补全 Yuni/Codis 项目的 API 文档。先用脚本扫描 Go 路由注册点生成草稿，再回看 handler、请求结构体、proto 与状态码定义补齐脚本无法静态推断的字段。生成给用户阅读的 Markdown 正文不展示源码来源和 handler 名称；这些信息只保留在 `_index.json` 中用于定位代码。

## Workflow

1. 确认仓库根目录和输出目录；用户未指定时，默认仓库根目录为当前目录，输出目录为 `<repo>/docs/api-docs`。
2. 阅读 `references/ims-framework.md`，确认本项目的 HTTP 接口、cmd 接口和 `ImjCommand` 响应包装规则。
3. 运行 `scripts/generate_api_doc_stubs.py` 生成 `_index.json` 和每接口一个 Markdown 草稿。
4. 查看 `_index.json` 中的 `source_file`、`handler`、`auth_required`、`needs_manual_completion` 字段，决定需要回看的 handler；不要把 `source_file` 或 `handler` 写入面向用户的 Markdown 文档正文。
5. 对每个草稿按 `references/http_api_template.md` 或 `references/cmd_api_template.md` 补齐中文短标题、请求参数、响应参数、请求示例、响应示例和状态码。
6. 如果字段来自 PB 生成代码，优先回看 `proto/pb/*.proto`，再结合 `proto/*.imj.go` 中的 `GetXxx`、`SetXxx`、`DelXxx` 或通用 `Get`、`Set`、`Del` 判断业务字段。
7. 状态码必须回看定义并写实际返回到 `head.ec` 或 HTTP status 的数字；不要把 Go 常量名放进状态码列。
8. 保持“一接口一文件”，按业务前缀放到子目录中，例如 `file.info` 放到 `file/file.info.md`。

## Quick Start

```bash
python3 ~/.codex/skills/yuni-api-docs/scripts/generate_api_doc_stubs.py \
  --repo-root /path/to/codis \
  --output-dir /path/to/codis/docs/api-docs \
  --overwrite
```

如果真实部署地址存在统一前缀，追加 `--route-prefix /v1/cos`，脚本会把该前缀写入请求示例。

## Documentation Rules

- 所有说明文字使用中文，字段名、命令名、路由、Go 常量名保持源码原样。
- Markdown 一级标题必须是简短中文业务描述，例如 `# 相册文件同步`、`# 查询文件详情`；不要把 cmd、路由、handler 名称或 Go 常量表达式作为标题，例如不要写 `# dir_files.sync`。
- 接口简介必须描述该接口的业务功能，例如“查询文件详情”“创建相册目录”；不要直接复制 cmd、路由或 handler 名称作为简介。脚本无法推断功能时保留 TODO，人工回看实现后再补。
- 面向用户的 Markdown 文档正文不要包含“来源”“source_file”“handler”或“Handler”字段；需要定位代码时只查 `_index.json`。
- HTTP 接口按普通 HTTP 语义描述路由、方法、header、query、path、body 参数。
- cmd 接口固定写 `接口: /v1/cmd`、`请求方法: POST`，具体命令写入 `cmd` 字段，请求业务参数写入 `ImjCommand.body`。
- JSON 响应默认按 `ImjCommand` 描述：顶层包含 `body`、`cmd`、`head`，响应参数表只列 `body` 内业务字段。
- 如果接口返回文件流、二进制流或透传下载，不要伪造 JSON 字段；在响应参数和响应示例中明确说明是流式返回。
- 状态码表必须列实际数字，例如 `200`、`10401`、`30405`，不要在“状态码”列写 `imjson.Codes.*` 或 `proto.SubCodes.*`。面向用户的说明写业务含义，例如 `请求成功`、`请求参数错误`，不要写“来源 xxx”。
- `imjson.Status` 带 `SubCode` 时，`ImjCommand.head.ec` 实际返回 `SubCode.Code`；例如 `imjson.Codes.InvalidParams` 应写 `10401`，不是 `400`。没有 `SubCode` 时写 `SysCode.Code`，例如 `Success=200`、`BadRequest=400`、`PermissionDeny=403`、`NotFound=404`、`InternalError=500`。
- `proto.SubCodes.*` 必须回看 `proto/state_codes.go` 等定义文件提取数字和中文说明，例如 `DirectoryExist=30405`。
- 受保护接口的鉴权写 HTTP 请求头 `Authorization`，不要写进 `ImjCommand.head`。
- 脚本生成的 `TODO` 必须回看代码后处理，无法确认时保留明确的“待确认”说明，不要凭空补字段。

## Resources

- `scripts/generate_api_doc_stubs.py`：扫描 ims 路由注册点并生成 Markdown 草稿。
- `references/ims-framework.md`：用户提供的 ims 框架、HTTP 接口、cmd 接口和 `ImjCommand` 说明。
- `references/http_api_template.md`：HTTP 接口文档模板。
- `references/cmd_api_template.md`：cmd 接口文档模板。
- `references/extraction-rules.md`：脚本提取范围与人工补全清单。
