# 课程0：初识 NoneBot2

欢迎来到 NoneBot2 的世界，这是一个由代码构成的机器人之城

NoneBot2 是一个现代、跨平台、可扩展的 Python 聊天机器人框架

由于基于 Python 的类型注解和异步特性，所以能够你的需求实现提供便捷灵活的支持，以及编辑器等支持

有关 NoneBot2 和 QQ 机器人的更多信息可参阅《使用NoneBot2搭建QQ机器人》

## 相关资料

NoneBot2 文档：[https://v2.nonebot.dev](http://v2.nonebot.dev/)

OneBot 适配器文档：[https://onebot.adapters.nonebot.dev](https://onebot.adapters.nonebot.dev/)

NoneBot2 新文档：[https://github.com/Well2333/nonebot2-tutorial](https://github.com/Well2333/nonebot2-tutorial)

《使用NoneBot2搭建QQ机器人》 Well404 编写：[https://github.com/Well2333/NoneBot2_NoobGuide](https://github.com/Well2333/NoneBot2_NoobGuide)

go-cqhttp 文档：[http://docs.go-cqhttp.org](http://docs.go-cqhttp.org/)

## NoneBot2 与 QQ 交互必不可少的一样东西——适配器（Adapter）

协议适配器用于将协议端上报的原始数据转换为 NoneBot2 的 `Event` 对象，用于分发给插件进行响应

如果把 NoneBot2 和协议端比作两名客户，他们的母语不同，适配器在这里起到了翻译的作用

由于协议有很多，就像世界上有很多种语言，一个翻译无法全部胜任全部语言的翻译工作，所以就需要一次招募多个翻译

同样，NoneBot2 也不知道需要什么翻译，所以需要在运行之前告知需要招募什么语种的翻译

这个过程叫 **注册协议适配器**

事实上，你目前所看到的终端便是由 Console 适配器所驱动的

QQ 机器人有两种驱动器支持——OneBot（V11 和 V12） 和 Mirai2
前者为 NoneBot 官方维护，后者为社区维护
本教程将使用 OneBot V11 适配器 + go-cqhttp 作为讲解
以及教你如何配置它们之间的连接

## 配置 go-cqhttp

前往 go-cqhttp 的 Release 界面：[https://github.com/Mrs4s/go-cqhttp/releases](https://github.com/Mrs4s/go-cqhttp/releases)，根据系统和架构下载最新版 go-cqhttp （如果是需要安装的包则安装）

运行 go-cqhttp，选择 **反向 WebSocket**

编辑配置文件 `config.yml` 成功登陆后，再次编辑 `config.yml`，翻到底部，会有下面的一段配置

```yml
# 反向WS设置
- ws-reverse:
    # 反向WS Universal 地址
    # 注意 设置了此项地址后下面两项将会被忽略
    universal: ws://your_websocket_universal.server
    # 反向WS API 地址
    api: ws://your_websocket_api.server
    # 反向WS Event 地址
    event: ws://your_websocket_event.server
    # 重连间隔 单位毫秒
    reconnect-interval: 3000
    middlewares:
      <<: *default # 引用默认中间件
```

其中 `universal` 的格式为 `ws://NoneBot2地址:端口/onebot/v11/ws/`

你应该将其设置为 `ws://{host}:{port}/onebot/v11/ws/`

重启 go-cqhttp，你应该会发现 go-cqhttp 输出下面的日志：

`[WARNING]: 连接到反向WebSocket Universal服务器 ws://{host}:{port}/onebot/v11/ws/ 时出现错误: websocket: bad handshake.`

同时 NoneBot 端也会出现日志：

`[INFO] uvicorn | ('127.0.0.1', xxxx) - "WebSocket /onebot/v11/ws/" 403`

这时你就需要在 Bot 入口文件（通常为 `bot.py` ）注册协议适配器

注册协议适配器需要导入对应协议适配器的 `Adapter`，以及获取驱动器来注册（注册适配器请务必在 `nonebot.init()` 之后注册）

注册 OneBot V11 适配器的代码如下

```python
import nonebot
from nonebot.adapter.onebot.v11 import Adapter  # 导入适配器
...
driver.register_adapter(Adapter)  # 注册适配器
```

重启 NoneBot2，这时 go-cqhttp 应该输出如下日志

`[INFO]: 已连接到反向WebSocket Universal服务器 ws://{host}:{port}/onebot/v11/ws/`

这时就恭喜你成功与 QQ 建立了联系，可以正式开启 Bot 之路了

### 练习0-1

注册 OneBot V11 适配器

执行完毕后，重启 NoneBot2

**此控制台输入将关闭，之后的课程需要在 QQ 中发送命令才可使用**
