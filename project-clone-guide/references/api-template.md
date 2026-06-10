# {模块名称}接口说明

> 每一个接口都必须重复填写以下完整区块。即使同一模块有多个接口，也不能只给一个共用示例；每个接口都要有独立、完整、可运行的请求示例和对应响应示例。

## 接口: `{路由}`

## 接口简介

{详细描述接口能做什么、触发什么业务流程、会读写哪些核心资源。}

## 请求方法

`{GET|POST|PUT|PATCH|DELETE|...}`

## 参数

| 名称 | 参数类型 | 类型 | 说明 | 必选 |
| --- | --- | --- | --- | --- |
| {字段名} | {Http Header / Http Body Json / Http Body Form / Router 查询参数 / Router 路径参数} | {int / string / bool / object / array / ...} | {参数作用} | {true/false} |

## 响应参数

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| {字段名} | {int / string / bool / object / array / ...} | {字段含义} |

## 请求示例

必须包含该接口的完整调用方式：请求方法、完整路由、路径参数、查询参数、必需 Header、Content-Type，以及该接口实际需要的 JSON/Form Body。接口不接收 Body 时，不要添加空的 `--data-raw`。

```bash
curl --location --request {METHOD} 'https://example.com{路由}' \
  --header 'Authorization: Bearer <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  }'
```

## 响应示例

必须包含该接口的完整响应结构，包含统一响应包裹字段以及该接口实际返回的代表性 `body` 字段。不要在 JSON 代码块里写注释；未能从代码确认的字段，在示例后用文字说明。

```json
{
  "body": {},
  "cmd": "{路由}",
  "head": {
    "ec": 200,
    "em": "请求成功",
    "is_response": true,
    "timestamp": 1767868031,
    "version": "1.0"
  }
}
```

## 状态码

| 状态码 | 说明 |
| --- | --- |
| {业务状态码} | {说明} |

## 业务流程

1. {handler/controller 接收请求并解析参数}
2. {service/domain 执行业务校验和核心逻辑}
3. {repository/client 访问数据库或外部服务}
4. {构造响应或错误}

## 代码证据

| 信息 | 代码位置 |
| --- | --- |
| 路由注册 | `{文件路径:行号}` |
| 请求解析 | `{文件路径:行号}` |
| 业务逻辑 | `{文件路径:行号}` |
| 响应结构 | `{文件路径:行号}` |
| 状态码 | `{文件路径:行号}` |
