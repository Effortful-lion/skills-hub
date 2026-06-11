#!/usr/bin/env python3
"""扫描 ims 路由注册点并生成 Markdown 接口文档草稿。"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, List, Sequence


HTTP_MARKERS = (
    "ims.HttpRSETRouter",
    "ims.HttpRouter",
    "ims.HttpRouterNoVerify",
    "ims.HttpRESTRouterNoVerify",
)

CMD_MARKERS = (
    "ims.WithImjHandler",
    "ims.WithImjHandlerNoVerify",
)

TITLE_OVERRIDES = {
    "/attach/upload": "附件上传",
    "/file/:fid": "文件下载",
    "/file/:fid/attach/:attach_id": "附件下载",
    "/file/:fid/attach/:attach_id/:path": "附件路径下载",
    "/file/multipart/abort/:fid": "分片上传取消",
    "/file/multipart/complete/:fid": "分片上传完成",
    "/file/multipart/init/:fid": "分片上传初始化",
    "/file/multipart/upload/:fid": "分片上传",
    "/file/upload/:fid": "文件上传",
    "/lambda/media/metrics": "媒体指标查询",
    "/lambda/node/:process": "媒体节点处理",
    "/lambda/node/list": "媒体节点列表查询",
    "/lambda/task/finish": "媒体任务完成",
    "/lambda/task/retry/:tid": "媒体任务重试",
    "/lambda/task/retrybyfid": "按文件重试媒体任务",
    "/lambda/workflow/:process": "媒体工作流处理",
    "/lambda/workflow/list": "媒体工作流列表查询",
    "/origin/auth": "源站鉴权",
    "/presign/access/:ticket": "预签名票据访问",
    "/presign/url": "预签名地址签发",
    "/s3/identity/auth": "S3 身份鉴权",
    "/s3/notification/*": "S3 事件通知接收",
    "/s3/security/auth": "S3 安全鉴权",
    "/s3/sts/credit": "S3 临时凭证获取",
    "attach.delete": "附件删除",
    "attach.info": "附件详情查询",
    "attach.list": "附件列表查询",
    "attach.update": "附件更新",
    "common.PluginCommand.PluginList": "插件列表查询",
    "common.PluginCommand.PluginRegisterPlugin": "插件注册",
    "common.PluginCommand.PluginUnRegisterPlugin": "插件注销",
    "console.activity-list": "控制台活动列表查询",
    "directory.create": "目录创建",
    "directory.delete": "目录删除",
    "directory.files": "目录文件查询",
    "directory.info": "目录详情查询",
    "directory.list": "目录列表查询",
    "dir_files.sync": "相册文件同步",
    "dirlist.sync": "相册列表同步",
    "event.list": "事件列表查询",
    "file.copy": "文件复制",
    "file.create": "文件创建",
    "file.delete": "文件删除",
    "file.info": "文件详情查询",
    "file.list": "文件列表查询",
    "file.metas": "文件元数据批量查询",
    "file.move": "文件移动",
    "file.tagging": "文件标签查询",
    "file.update.data": "文件数据更新",
    "file.update.meta": "文件元数据更新",
    "file.update.moreinfo": "文件扩展信息更新",
    "plugin.list": "插件列表查询",
    "plugin.register": "插件注册",
    "plugin.unregister": "插件注销",
    "space.global.info": "全局空间信息查询",
    "space.userInDir.infos": "目录用户空间信息查询",
    "user.info": "用户信息查询",
    "user.login": "用户登录",
}

DOMAIN_LABELS = {
    "access": "访问",
    "activity": "活动",
    "attach": "附件",
    "console": "控制台",
    "dir_files": "相册文件",
    "directory": "目录",
    "dirlist": "相册列表",
    "event": "事件",
    "fid": "文件",
    "file": "文件",
    "files": "文件",
    "global": "全局",
    "identity": "身份",
    "lambda": "媒体任务",
    "media": "媒体",
    "multipart": "分片上传",
    "node": "节点",
    "origin": "源站",
    "presign": "预签名",
    "s3": "S3",
    "security": "安全",
    "space": "空间",
    "sts": "临时凭证",
    "task": "任务",
    "ticket": "票据",
    "user": "用户",
    "workflow": "工作流",
}

OPERATION_LABELS = {
    "abort": "取消",
    "auth": "鉴权",
    "complete": "完成",
    "copy": "复制",
    "create": "创建",
    "credit": "获取",
    "delete": "删除",
    "finish": "完成",
    "info": "详情查询",
    "infos": "信息查询",
    "init": "初始化",
    "list": "列表查询",
    "login": "登录",
    "metas": "元数据查询",
    "metrics": "指标查询",
    "move": "移动",
    "notification": "通知接收",
    "process": "处理",
    "register": "注册",
    "retry": "重试",
    "retrybyfid": "按文件重试",
    "sync": "同步",
    "tagging": "标签查询",
    "unregister": "注销",
    "upload": "上传",
    "url": "地址签发",
}


@dataclass
class ParamRow:
    """描述文档参数表中的一行。"""

    name: str
    location: str
    data_type: str
    description: str
    required: str


@dataclass
class RouteDoc:
    """保存单个接口文档草稿需要的元数据。"""

    kind: str
    title: str
    route: str
    methods: List[str]
    command: str
    handler: str
    source_file: str
    source_line: int
    auth_required: bool
    description: str
    params: List[ParamRow] = field(default_factory=list)
    needs_manual_completion: List[str] = field(default_factory=list)


# build_parser 构建命令行参数解析器。
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="扫描 ims 路由注册点并生成 Markdown 接口文档草稿")
    parser.add_argument("--repo-root", required=True, help="Go 项目根目录")
    parser.add_argument("--output-dir", required=True, help="Markdown 文档输出目录")
    parser.add_argument("--route-prefix", default="", help="请求示例中的统一路由前缀")
    parser.add_argument("--overwrite", action="store_true", help="允许覆盖已存在的 Markdown 草稿")
    return parser


# collect_go_files 收集仓库中需要扫描的 Go 源文件。
def collect_go_files(repo_root: Path) -> List[Path]:
    result: List[Path] = []
    for path in repo_root.rglob("*.go"):
        relative_parts = path.relative_to(repo_root).parts
        # 跳过依赖目录和隐藏目录，减少误匹配。
        if any(part in {"vendor", ".git"} or part.startswith(".") for part in relative_parts):
            continue
        if path.name.endswith("_test.go"):
            continue
        result.append(path)
    return sorted(result)


# read_text 读取源码文本并容忍少量不可解码字符。
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


# line_number_for_offset 将源码偏移量换算为行号。
def line_number_for_offset(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


# find_matching_paren 找到与指定左括号匹配的右括号。
def find_matching_paren(source: str, open_index: int) -> int:
    depth = 0
    in_double = False
    in_single = False
    in_backtick = False
    in_line_comment = False
    in_block_comment = False
    escaped = False

    for index in range(open_index, len(source)):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""

        if in_line_comment:
            if char == "\n":
                in_line_comment = False
            continue
        if in_block_comment:
            if char == "*" and next_char == "/":
                in_block_comment = False
            continue
        if in_double:
            if char == '"' and not escaped:
                in_double = False
            escaped = char == "\\" and not escaped
            continue
        if in_single:
            if char == "'" and not escaped:
                in_single = False
            escaped = char == "\\" and not escaped
            continue
        if in_backtick:
            if char == "`":
                in_backtick = False
            continue

        if char == "/" and next_char == "/":
            in_line_comment = True
            continue
        if char == "/" and next_char == "*":
            in_block_comment = True
            continue
        if char == '"':
            in_double = True
            escaped = False
            continue
        if char == "'":
            in_single = True
            escaped = False
            continue
        if char == "`":
            in_backtick = True
            continue

        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    return -1


# split_top_level_args 将函数调用参数按顶层逗号拆分。
def split_top_level_args(raw_args: str) -> List[str]:
    args: List[str] = []
    current: List[str] = []
    depth_paren = 0
    depth_brace = 0
    depth_bracket = 0
    in_double = False
    in_single = False
    in_backtick = False
    escaped = False

    for char in raw_args:
        if in_double:
            current.append(char)
            if char == '"' and not escaped:
                in_double = False
            escaped = char == "\\" and not escaped
            continue
        if in_single:
            current.append(char)
            if char == "'" and not escaped:
                in_single = False
            escaped = char == "\\" and not escaped
            continue
        if in_backtick:
            current.append(char)
            if char == "`":
                in_backtick = False
            continue

        if char == '"':
            in_double = True
            escaped = False
        elif char == "'":
            in_single = True
            escaped = False
        elif char == "`":
            in_backtick = True
        elif char == "(":
            depth_paren += 1
        elif char == ")":
            depth_paren -= 1
        elif char == "{":
            depth_brace += 1
        elif char == "}":
            depth_brace -= 1
        elif char == "[":
            depth_bracket += 1
        elif char == "]":
            depth_bracket -= 1

        # 只在顶层逗号处拆分，避免拆坏数组、结构体字面量和嵌套调用。
        if char == "," and depth_paren == 0 and depth_brace == 0 and depth_bracket == 0:
            arg = "".join(current).strip().rstrip(",").strip()
            if arg:
                args.append(arg)
            current = []
            continue
        current.append(char)

    tail = "".join(current).strip()
    if tail:
        args.append(tail)
    return args


# unquote 去掉 Go 字符串字面量的外层引号。
def unquote(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "`"}:
        return value[1:-1]
    return value


# first_string_literal 提取表达式中的第一个字符串字面量。
def first_string_literal(raw: str) -> str:
    match = re.search(r'"([^"\\]*(?:\\.[^"\\]*)*)"', raw)
    if match:
        return bytes(match.group(1), "utf-8").decode("unicode_escape")
    match = re.search(r"`([^`]*)`", raw)
    return match.group(1) if match else ""


# parse_methods 从 HTTP 方法参数中提取方法列表。
def parse_methods(raw: str) -> List[str]:
    methods: List[str] = []
    for method in re.findall(r"http\.Method([A-Za-z]+)", raw):
        methods.append(method.upper())
    for method in re.findall(r'"([A-Z]+)"', raw):
        methods.append(method.upper())
    return methods or ["POST"]


# extract_handler_name 提取 handler 表达式中最适合展示的名称。
def extract_handler_name(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    value = value.split("//", 1)[0].strip()
    return value.rsplit(".", 1)[-1]


# extract_api_description 从路由参数中提取 apiDescMiddleware 文案。
def extract_api_description(raw_args: str) -> str:
    match = re.search(r"apiDescMiddleware\(\s*([\"`])(?P<desc>.*?)(?<!\\)\1\s*\)", raw_args, re.S)
    if match:
        return match.group("desc").strip()
    return ""


# contains_cjk 判断文本中是否包含中文字符。
def contains_cjk(value: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", value))


# concise_title_from_description 从接口描述中提取适合作为标题的中文短句。
def concise_title_from_description(description: str) -> str:
    value = description.strip()
    if not contains_cjk(value) or "TODO" in value or "待确认" in value:
        return ""
    value = re.split(r"[，。；;,.!！?？\n]", value, maxsplit=1)[0].strip()
    value = re.sub(r"^(该接口)?用于", "", value).strip()
    if len(value) <= 24:
        return value
    return ""


# identifier_tokens 将路由或 cmd 名称拆成可翻译的业务词元。
def identifier_tokens(raw: str) -> List[str]:
    value = raw.strip()
    value = re.sub(r"^common\.PluginCommand\.Plugin", "plugin.", value)
    value = value.strip("/")
    value = value.replace("*", "wildcard")
    value = re.sub(r":[A-Za-z_][A-Za-z0-9_]*", "", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    tokens = [token.lower() for token in re.split(r"[/._-]+", value) if token]
    return [token for token in tokens if token not in {"v1", "cmd", "wildcard", "path", "id"}]


# title_from_identifier 根据路由或 cmd 名称生成中文短标题。
def title_from_identifier(raw: str) -> str:
    if raw in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[raw]
    tokens = identifier_tokens(raw)
    if not tokens:
        return ""
    operation_index = -1
    operation = ""
    for index in range(len(tokens) - 1, -1, -1):
        token = tokens[index]
        if token in OPERATION_LABELS:
            operation_index = index
            operation = OPERATION_LABELS[token]
            break
    domain_tokens = tokens[:operation_index] if operation_index >= 0 else tokens
    domain_parts = []
    for token in domain_tokens:
        if token in DOMAIN_LABELS:
            label = DOMAIN_LABELS[token]
            if label not in domain_parts:
                domain_parts.append(label)
    domain = "".join(domain_parts)
    if domain and operation:
        return domain + operation
    if operation:
        return operation
    if domain:
        return domain + "接口"
    return ""


# resolve_title 生成面向用户的中文短标题。
def resolve_title(kind: str, route_or_command: str, description: str = "") -> str:
    title = concise_title_from_description(description)
    if title:
        return title
    title = title_from_identifier(route_or_command)
    if title:
        return title
    label = "cmd 命令" if kind == "cmd" else "路由"
    value = route_or_command.strip() or "待确认"
    return f"TODO: 补充简短中文标题，描述 {label} `{value}` 的业务动作。"


# fallback_description 生成需要人工补全的接口功能说明占位。
def fallback_description(kind: str, route_or_command: str) -> str:
    label = "cmd 命令" if kind == "cmd" else "路由"
    value = route_or_command.strip() or "待确认"
    return f"TODO: 回看接口实现后补充功能说明，说明该接口用于完成什么业务功能；不要直接复制 {label} `{value}`。"


# path_params_from_route 从 HTTP 路由中推导 path 参数。
def path_params_from_route(route: str) -> List[ParamRow]:
    params: List[ParamRow] = []
    for name in re.findall(r":([A-Za-z_][A-Za-z0-9_]*)", route):
        params.append(ParamRow(name=name, location="Router(Path)", data_type="string", description="路径参数", required="是"))
    if "*" in route:
        params.append(ParamRow(name="wildcard", location="Router(Path)", data_type="string", description="通配路径", required="否"))
    return params


# auth_params 根据鉴权信息生成请求头参数。
def auth_params(auth_required: bool) -> List[ParamRow]:
    if not auth_required:
        return []
    return [
        ParamRow(
            name="Authorization",
            location="Http Header",
            data_type="string",
            description="访问令牌",
            required="是",
        )
    ]


# normalize_doc_name 将路由或命令转换为稳定文件名。
def normalize_doc_name(raw: str) -> str:
    value = raw.strip().strip("/")
    value = value.replace(":", "").replace("*", "wildcard")
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "api"


# category_for_route 根据接口名称推导输出子目录。
def category_for_route(route_doc: RouteDoc) -> str:
    if route_doc.kind == "cmd":
        first = route_doc.command.split(".", 1)[0]
        return normalize_doc_name(first) or "cmd"
    for part in route_doc.route.strip("/").split("/"):
        if not part or part.startswith(":") or re.fullmatch(r"v\d+", part):
            continue
        return normalize_doc_name(part)
    return "misc"


# full_url 拼接请求示例中的路由地址。
def full_url(route_prefix: str, route: str) -> str:
    prefix = route_prefix.strip()
    if prefix and not prefix.startswith("/"):
        prefix = "/" + prefix
    return "{{base_url}}" + prefix.rstrip("/") + "/" + route.lstrip("/")


# shell_quote_json 生成 curl 示例中可读的 JSON 字符串。
def shell_quote_json(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


# render_param_rows 渲染请求参数表。
def render_param_rows(params: Sequence[ParamRow]) -> str:
    if not params:
        return "| 暂无 | - | - | 无需参数或待确认 | 否 |"
    lines = []
    for param in params:
        lines.append(f"| {param.name} | {param.location} | {param.data_type} | {param.description} | {param.required} |")
    return "\n".join(lines)


# render_curl 渲染请求示例。
def render_curl(route_doc: RouteDoc, route_prefix: str) -> str:
    method = route_doc.methods[0] if route_doc.methods else "POST"
    headers = ["--header 'Content-Type: application/json'"]
    if route_doc.auth_required:
        headers.append("--header 'Authorization: Bearer {{token}}'")
    if route_doc.kind == "cmd":
        payload = {"cmd": route_doc.command, "body": {}}
        return "\n".join(
            [
                f"curl --location --request POST '{full_url(route_prefix, '/v1/cmd')}' \\",
                *[f"{header} \\" for header in headers],
                f"--data-raw '{shell_quote_json(payload)}'",
            ]
        )
    if method in {"GET", "HEAD", "OPTIONS"}:
        lines = [f"curl --location --request {method} '{full_url(route_prefix, route_doc.route)}' \\"]
        for index, header in enumerate(headers):
            suffix = " \\" if index < len(headers) - 1 else ""
            lines.append(f"{header}{suffix}")
        return "\n".join(lines)
    return "\n".join(
        [
            f"curl --location --request {method} '{full_url(route_prefix, route_doc.route)}' \\",
            *[f"{header} \\" for header in headers],
            "--data-raw '{}'",
        ]
    )


# render_response_example 渲染默认响应示例。
def render_response_example(route_doc: RouteDoc) -> str:
    cmd_value = route_doc.command if route_doc.kind == "cmd" else route_doc.route
    payload = {
        "body": {},
        "cmd": cmd_value,
        "head": {
            "ec": 200,
            "em": "请求成功",
            "is_response": True,
            "timestamp": 0,
            "version": "1.0",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# render_markdown 渲染单个接口 Markdown 草稿。
def render_markdown(route_doc: RouteDoc, route_prefix: str) -> str:
    cmd_line = f"- cmd: {route_doc.command}\n" if route_doc.kind == "cmd" else ""
    manual_items = "\n".join(f"- TODO: {item}" for item in route_doc.needs_manual_completion)
    return f"""# {route_doc.title}

- 接口: {route_doc.route}
{cmd_line}- 请求方法: {", ".join(route_doc.methods)}
- 是否鉴权: {"是" if route_doc.auth_required else "否"}
- 接口简介: {route_doc.description}

- 参数：

| 属性 | 参数位置 | 类型 | 说明 | 必选 |
| --- | --- | --- | --- | --- |
{render_param_rows(route_doc.params)}

- 响应参数：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| body | object | TODO: 回看接口实现的成功返回分支后补齐 body 内字段 |

- 请求示例：

```bash
{render_curl(route_doc, route_prefix)}
```

- 响应示例：

```json
{render_response_example(route_doc)}
```

- 状态码：

| 状态码 | 说明 |
| --- | --- |
| 200 | 请求成功 |
| TODO | 回看 imjson.Codes.* 或 proto.SubCodes.* 定义后补齐实际数字；禁止直接写 Go 常量名 |

- 人工补全：

{manual_items}
"""


# parse_http_route 将 HTTP 注册调用解析为 RouteDoc。
def parse_http_route(marker: str, args: Sequence[str], raw_args: str, source_file: Path, repo_root: Path, line: int) -> RouteDoc | None:
    if len(args) < 3:
        return None
    route = first_string_literal(args[1]) or unquote(args[1])
    handler = extract_handler_name(args[2])
    auth_required = "NoVerify" not in marker and "OinRouterNoVerify" not in raw_args
    api_description = extract_api_description(raw_args)
    description = api_description or fallback_description("http", route)
    title = resolve_title("http", route, description)
    params = auth_params(auth_required) + path_params_from_route(route)
    return RouteDoc(
        kind="http",
        title=title,
        route=route,
        methods=parse_methods(args[0]),
        command="",
        handler=handler,
        source_file=str(source_file.relative_to(repo_root)),
        source_line=line,
        auth_required=auth_required,
        description=description,
        params=params,
        needs_manual_completion=["补齐接口实现中读取的 query、header、body 或 form 参数", "补齐 body 内响应字段", "补齐业务状态码实际数字"],
    )


# parse_cmd_route 将 cmd 注册调用解析为 RouteDoc。
def parse_cmd_route(marker: str, args: Sequence[str], raw_args: str, source_file: Path, repo_root: Path, line: int) -> RouteDoc | None:
    if len(args) < 2:
        return None
    command = first_string_literal(args[0]) or unquote(args[0])
    handler = extract_handler_name(args[1])
    auth_required = "NoVerify" not in marker
    description = fallback_description("cmd", command)
    title = resolve_title("cmd", command, description)
    params = auth_params(auth_required)
    params.append(ParamRow(name="cmd", location="ImjCommand.cmd", data_type="string", description="cmd 接口命令名", required="是"))
    params.append(ParamRow(name="body", location="ImjCommand.body", data_type="object", description="TODO: 回看接口实现补齐业务参数", required="否"))
    return RouteDoc(
        kind="cmd",
        title=title,
        route="/v1/cmd",
        methods=["POST"],
        command=command,
        handler=handler,
        source_file=str(source_file.relative_to(repo_root)),
        source_line=line,
        auth_required=auth_required,
        description=description,
        params=params,
        needs_manual_completion=["补齐 ImjCommand.body 请求字段", "补齐 body 内响应字段", "补齐业务状态码实际数字"],
    )


# iter_marker_calls 遍历源码中的指定 ims 注册调用。
def iter_marker_calls(source: str, marker: str) -> Iterable[tuple[int, str]]:
    search_from = 0
    while True:
        marker_index = source.find(marker, search_from)
        if marker_index == -1:
            break
        marker_end = marker_index + len(marker)
        if marker_end < len(source) and re.match(r"[A-Za-z0-9_]", source[marker_end]):
            # 避免短 marker 误匹配长函数名，例如 HttpRouter 匹配到 HttpRouterNoVerify。
            search_from = marker_end
            continue
        open_index = source.find("(", marker_index + len(marker))
        if open_index == -1:
            break
        close_index = find_matching_paren(source, open_index)
        if close_index == -1:
            search_from = open_index + 1
            continue
        yield marker_index, source[open_index + 1:close_index]
        search_from = close_index + 1


# scan_routes 扫描所有 Go 文件并生成接口元数据列表。
def scan_routes(repo_root: Path) -> List[RouteDoc]:
    docs: List[RouteDoc] = []
    for source_file in collect_go_files(repo_root):
        source = read_text(source_file)
        for marker in HTTP_MARKERS:
            for marker_index, raw_args in iter_marker_calls(source, marker):
                args = split_top_level_args(raw_args)
                line = line_number_for_offset(source, marker_index)
                doc = parse_http_route(marker, args, raw_args, source_file, repo_root, line)
                if doc:
                    docs.append(doc)
        for marker in CMD_MARKERS:
            for marker_index, raw_args in iter_marker_calls(source, marker):
                args = split_top_level_args(raw_args)
                line = line_number_for_offset(source, marker_index)
                doc = parse_cmd_route(marker, args, raw_args, source_file, repo_root, line)
                if doc:
                    docs.append(doc)
    return sorted(docs, key=lambda item: (item.kind, item.source_file, item.source_line, item.command or item.route))


# output_path_for 计算接口文档输出路径。
def output_path_for(output_dir: Path, route_doc: RouteDoc) -> Path:
    category = category_for_route(route_doc)
    base_name = normalize_doc_name(route_doc.command if route_doc.kind == "cmd" else route_doc.route)
    return output_dir / category / f"{base_name}.md"


# write_outputs 写入 Markdown 草稿和索引文件。
def write_outputs(docs: Sequence[RouteDoc], output_dir: Path, route_prefix: str, overwrite: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    index_rows = []
    for doc in docs:
        target = output_path_for(output_dir, doc)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not overwrite:
            raise FileExistsError(f"{target} already exists; rerun with --overwrite to replace generated stubs")
        target.write_text(render_markdown(doc, route_prefix), encoding="utf-8")
        row = asdict(doc)
        row["doc_file"] = str(target.relative_to(output_dir))
        index_rows.append(row)
    index_file = output_dir / "_index.json"
    if index_file.exists() and not overwrite:
        raise FileExistsError(f"{index_file} already exists; rerun with --overwrite to replace generated index")
    index_file.write_text(json.dumps(index_rows, ensure_ascii=False, indent=2), encoding="utf-8")


# main 执行扫描和文档生成流程。
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not repo_root.exists():
        parser.error(f"repo root not found: {repo_root}")
    docs = scan_routes(repo_root)
    write_outputs(docs, output_dir, args.route_prefix, args.overwrite)
    print(f"generated {len(docs)} api doc stubs into {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
