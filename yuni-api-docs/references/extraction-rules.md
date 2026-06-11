# 提取规则与人工补全清单

## 脚本自动提取

1. HTTP 路由注册点：`ims.HttpRSETRouter`、`ims.HttpRouter`、`ims.HttpRouterNoVerify`、`ims.HttpRESTRouterNoVerify`。
2. cmd 路由注册点：`ims.WithImjHandler`、`ims.WithImjHandlerNoVerify`。
3. HTTP 方法：从 `[]string{http.MethodGet, http.MethodPost}` 或字符串字面量中提取。
4. HTTP 路由：从注册函数第二个参数提取。
5. cmd 命令：从注册函数第一个参数提取；如果是常量 selector 且无法静态解析，保留源码表达式。
6. handler：从注册函数参数中提取最后一级函数或方法名，仅写入 `_index.json` 供人工补全时定位代码，不写入 Markdown 正文。
7. 接口说明：优先读取 `apiDescMiddleware("...")`；没有描述时生成 TODO 功能说明占位，人工回看实现后补成“该接口用于做什么”的业务说明，不要直接复制路由、cmd 或 handler 名称。
8. 鉴权：`NoVerify` 注册函数或参数中出现 `OinRouterNoVerify` 时标记为无需鉴权，其余默认需要鉴权。
9. 路径参数：从 HTTP 路由中的 `:name` 和 `*` 通配符生成参数占位。
10. 输出：生成 `_index.json` 和每个接口的 Markdown 草稿；Markdown 正文不包含来源文件、源码行号或 handler 名称。

## 必须人工补全

1. `body` 内具体请求字段和响应字段。
2. handler 内不同分支返回不同结构的响应示例。
3. `FormFile`、`QueryParam`、`Header.Get`、`Bind`、`Decode`、`ShouldBind*` 等 handler 内部读取的参数。
4. `imjson.Codes.*`、`proto.SubCodes.*` 的实际数字和中文业务状态码说明；状态码列禁止直接写 Go 常量名。
5. 文件流、二进制流、重定向、透传下载等非 JSON 响应。
6. 来自 `proto/*.imj.go` 或 `proto/pb/*.proto` 的字段定义。

## 补全顺序

1. 先打开 `_index.json`，按 `needs_manual_completion` 找到需要补齐的接口。
2. 回看 `source_file` 中的路由注册点，确认路由、方法、鉴权和描述。
3. 回看 `handler`，查找参数读取、成功返回分支和错误返回分支。
4. 如果出现结构体，搜索 `type Xxx struct` 和相关 tag；如果是 PB 生成结构，优先看 `proto/pb/*.proto`。
5. 更新 Markdown 中的接口简介、参数表、响应参数表、curl 示例、响应示例和状态码表；接口简介写业务功能说明，不写 cmd、路由或 handler 的重复文本。
6. 对每个 `AttachHead`、`JsonResponse`、`CloseWithStatus`、`WithSubCode` 分支，回看状态码定义并写实际数字：`imjson.Status` 有 `SubCode` 时写 `SubCode.Code`，否则写 `SysCode.Code`；`proto.SubCodes.*` 写定义中的 `Code` 数值。面向用户的状态码说明只写业务含义，不写“来源 xxx”。
