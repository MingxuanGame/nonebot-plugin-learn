"""课程1：插件入门"""

from io import BytesIO
from pathlib import Path
from typing import List, Optional

from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot import get_loaded_plugins
from nonebot_plugin_imageutils import text2image
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment

from ...bbcode import Link
from ...bbcode import Path as BBPath
from ...state import STATES, set_state
from ...bbcode import Quote, Command, Exercise

TUTORIAL = f"""课程1：插件入门
文档地址：教程 > 插件 > 插件入门
{Link('https://v2.nonebot.dev/docs/tutorial/plugin/introduction')}

NoneBot2 中负责实现具体功能（例如表情包生成，面包店等）的最小模块称为插件（Plugin），也是用户对事件进行处理的基础单位。
接下来让我们引用一段话来说明插件与 NoneBot2 的关系：
{Quote('''假如说使用 NoneBot2 搭建的机器人是一个人的话，NoneBot2 框架可以理解为这个机器人的身体，能够做出各种各样的行为（例如发送消息），
但必须依赖于大脑产生的指令来活动，而自身并不会自主产生任意活动。而插件则是这个机器人的“大脑”，虽然自身并不能独立活动，
但可以通过向身体发出指令来执行其功能。''')}—— NoneBot2 新文档（由 Well404 编写）

接下来让我们了解插件的概念。
如果你对 Python 比较了解，那么应该不难理解{Command('模块')}（Module）和{Command('包')}（Package）的概念，
简而言之，模块就是一个 .py 文件，包是有一个名为 {Command('__init__.py')} 和若干模块、文件和包等组成的文件夹
NoneBot2 会将模块和包转换为插件，所以插件既可以是一个模块，也可以是一个包
现在让我们来创建一个插件：

{Exercise('1-1')}
前往 [color=#b97a56]%s[/color] 新建一个名为 {BBPath('hello_nonebot.py')} 的文件和 {BBPath('hello_bot')} 的包

执行完毕后，可发送 “{Command('提交课程1')}” 来提交结果"""


def get_plugin_path() -> Optional[Path]:
    manager = get_loaded_plugins().pop().manager
    if path := manager.search_path:
        return Path(list(path)[0]).absolute()


async def handle_tutorial1(matcher: Matcher, _: MessageEvent):
    logger.info(get_plugin_path())
    if get_plugin_path():
        img = text2image(TUTORIAL % get_plugin_path())
        output = BytesIO()
        img.save(output, format="png")
        await matcher.finish(MessageSegment.image(output))


def check_path(path: Path, name: str = "课程1") -> List[str]:
    module_is_exists = (path / "hello_nonebot.py").exists()
    dir_is_exists = (path / "hello_bot").exists()
    is_package = (path / "hello_bot" / "__init__.py").exists()
    error_msgs = []
    if not module_is_exists:
        error_msgs.append(f"{name}未达成条件：未新建文件 hello_nonebot.py")
    if not dir_is_exists:
        error_msgs.append(f"{name}未达成条件：未找到包 hello_bot")
    elif not is_package:
        error_msgs.append(
            f"{name}未达成条件：找到文件夹 hello_bot 但是未找到 hello_bot/__init__.py（不合法的包）"
        )
    return error_msgs


async def commit_tutorial1(matcher: Matcher, _: MessageEvent):
    if not (path := get_plugin_path()):
        return
    error_msgs = check_path(path)
    if error_msgs:
        await matcher.finish("提交结果失败：\n" + "\n".join(error_msgs))
    else:
        set_state("2")
        await matcher.finish(
            f"恭喜通过课程1，接下来的课程为：\n{STATES['2']}\n输入命令“课程2”进入"
        )


__tutorial1__ = {"课程1": handle_tutorial1, "提交课程1": commit_tutorial1}
