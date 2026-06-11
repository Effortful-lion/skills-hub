# 中文短标题

- 接口: [路由]
- cmd: [cmd name(只有 cmd 接口才需要这个)]
- 请求方法: [GET|POST....]
- 请求参数


    | 属性 | 类型 | 说明 | 必选 |
    | --- | --- | --- | --- |
    | xxxx | string | xxxxx | 是/否 |
- 响应参数：


    | 属性 | 类型 | 说明 |
    | --- | --- | --- |
    | xxxx | string | xxxxxx |
- 请求示例：

    ```bash
    curl --location --request POST '[请求地址]/v1/cmd' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "cmd": "[cmd name]",
        "body": {
            "xxxxx": "xxxxx",
            "xxxxx": "xxxx"
        }
    }'
    ```

- 响应示例：

    ```json
    {
        "body": {
            "xxx":"xxxx"
        },
        "cmd": "cmd name",
        "head": {
            "xxxx": "xxxx"
        }
    }
    ```

- 状态码：


    | 状态码 | 说明 |
    | --- | --- |
    | 200 | 请求成功 |
    | 10401 | 请求参数错误 |
