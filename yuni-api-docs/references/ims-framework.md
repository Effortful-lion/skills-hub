## ims 框架
ims 框架是基于 echo 框架自研的 im 框架，包含了 http 和 ws 两种协议。
ims 框架支持多种接口定义形式，可以分为两大类：
- http：
  - HttpRSETRouter：REST 类型的HTTP接口.
  - HttpRESTRouterNoVerify: 无需验证的 REST 类型的HTTP接口。
  - HttpRouter: HTTP 接口。
  - HttpRouterNoVerify: HTTP 接口，不进行验证。
- cmd:
  - WithImjHandler: 定义 cmd 接口。
  - WithImjHandlerNoVerify: 定义 cmd 接口，不进行验证。

## ImjCommand
ImjCommad 是我们定义的标准结构，包含三部分：
- cmd：这里存储的是接口的路由或者 cmd 名称，类型是string。
- body：存储的是接口的数据，类型可以看成是一个map[string]any。
- head：存储的是接口中的一些头部信息，与 http header 不一样，类型也是一个map[string]any。

```json
{
  "body": {},
  "cmd": "/v1/xxxxxx",
  "head": {}
}
```

## 接口定义
我们的系统中有两种接口，分别是：http 接口、cmd 接口
- http 接口：
  - 接口特点：接口的路由和输入输出与正常的 http 接口一致，区别在于接口的返回值，所有非流式响应的 http 接口响应值都是 ImjCommand 接口的，http 接口的路由会赋值给 ImjCommand 的 cmd。响应的数据会放在 ImjCommand 的 body 中，响应的一些业务头部信息会放在 ImjCommand 的 head 中，例如业务业务状态码 Ec，业务状态描述 Em 等等。
  - 定义方式：参考 ims 框架的http 接口。
  - 例如：
    ```json
        {
          "body": {
            "cpu": {
              "cores": 1,
              "usage": 16.83
            },
            "disk": {
              "total": 494384795648,
              "used": 241011503104
            },
            "memory": {
              "total": 25769803776,
              "used": 16402497536
             },
            "network": {
              "download_speed": 106,
              "speed": 104857600,
              "upload_speed": 141
            }
          },
          "cmd": "/v1/console/system/resource",
          "head": {
            "ec": 200,
            "em": "请求成功",
            "is_response": true,
            "timestamp": 1751862568,
            "version": "1.0"
          }
       }
    ```

- cmd 接口：
  - 接口特点：cmd 接口的路由固定为 /v1/cmd，请求方式为 POST，请求的输入和输出参数都是 ImjCommand 结构，ims 框架根据输入参数中的 cmd 来匹配对应的 Handler ，响应与 http 接口的响应一致。
  - 定义方式：参考 ims 框架的 cmd 接口。
  - 例如：
    - 请求：
      ```json
      {
        "cmd": "system.info"
      }
      ```
    - 响应：
      ```json
      {
       "body": {
          "cloud_disk_name": "admin的云盘",
          "description": {
            "content": "asdcasdasdasdasd",
            "title": "asdasdasasdasdasd"
          },
         "domain": "http://yn-photos-localhost.photos.uneedx.com"
       },
       "cmd": "system.info",
       "head": {
          "X-IM-Owner-DeviceId": "test_device_id",
          "X-IM-Owner-RealIP": "::1",
          "X-IM-Owner-SessionId": "10de553c-6ca7-4a39-a401-093e17be2715",
          "X-IM-Upstream-RealIP": "::1",
          "ec": 200,
          "em": "请求成功",
          "fin": true,
          "is_response": true,
          "owner_id": "yp_JuDQQgkOaG",
          "timestamp": 1770093827,
          "version": "1.0"
       }
      }
      ```