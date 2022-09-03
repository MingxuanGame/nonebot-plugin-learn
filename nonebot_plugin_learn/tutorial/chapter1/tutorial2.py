"""课程2：加载插件"""
from io import BytesIO
from pathlib import Path

from nonebot.matcher import Matcher
from nonebot import get_available_plugin_names
from nonebot_plugin_imageutils import text2image
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment

from .tutorial1 import check_path
from ...bbcode import Path as BBPath
from ...bbcode import Log, Bold, Link
from ...state import STATES, set_state
from ...bbcode import Error, Yellow, Command, Exercise

TUTORIAL = f"""课程2：加载插件
文档地址：教程 > 插件 > 加载插件
{Link('https://v2.nonebot.dev/docs/tutorial/plugin/load-plugin')}

在上一节课程中，我们已经新建了两个插件。
如果在进入本节课程前重启了 NoneBot2，
且未修改任何代码，那么你可能会在控制台看到下面的日志：
{Log(f'Succeeded to import "{Yellow("hello_nonebot")}"', "SUCCESS", "nonebot")}
{Log(f'Succeeded to import "{Yellow("hello_bot")}"', "SUCCESS", "nonebot")}
那么恭喜，你已经成功加载了两个插件

（下面的代码运行的前提是你已经 {Command('import nonebot')}）
上面加载两个插件的方法为{Bold('加载目录中插件')}，使用 {Command('load_plugins')} 可以做到加载目录中的所有插件
代码如下：
{Command('nonebot.load_plugins("目录")')}
例如你想加载 {BBPath('src')} 目录的插件，就可以使用
{Command('nonebot.load_plugins("src")')}
此函数也支持多个目录，如
{Command('nonebot.load_plugins("src", "plugins")')}
{Error(f'注意：导入插件的目录应该是相对于你的入口文件，例如 {BBPath("bot.py")}')}

但是如果你想导入一个从 PyPI 安装的插件，使用目录方式加载就不太现实了，这时候就可以使用 {Command('load_plugin')}
此函数用于{Bold('加载单个插件')}，代码如下
{Command('nonebot.load_plugin("插件包名/模块名")')}
例如需要加载一个服务器状态插件（nonebot_plugin_status），可以使用
{Command('nonebot.load_plugin("nonebot_plugin_status")')}
但是此函数单次只能加载一个插件，若需要同时加载多个插件，就需要 {Command('load_all_plugins')} 登场了
{Yellow(f'备注：在新版本中，此函数支持 {Command("pathlib.Path")} 了，会根据目录将其转换为模块/包形式（#1194）')}

load_all_plugins 需要传入两个列表（其实是可迭代对象就行）
第一个为模块/包形式的导入的列表（即 load_plugin 的参数）
第二个为目录列表（即 load_plugins 的参数）
使用 load_all_plugins 整合上面所讲的加载命令如下
{Command('nonebot.load_all_plugins(["nonebot_plugin_status"], ["src", "plugins"])')}

上面所介绍的 load_all_plugins 还有两个变种形式，我们讲解其中的一种 —— {Command('load_from_toml')}
{Command('load_from_json')} 的使用方法可自行查看文档（和 load_from_toml 差不多）
load_from_toml 通过读取 TOML 文件中的 {Command('[tool.nonebot]')} 表中的 {Command('plugins')} 和 {Command('plugin_dirs')}，
分别对应 load_all_plugins 的两个参数
修改 TOML 文件后，可以使用下面的代码加载 TOML 中填写的插件
{Command('nonebot.load_from_toml("TOML文件名")')}
{Error('注意：TOML 文件是相对于运行目录的')}
如果你使用 nb-cli 新建项目，那么项目中会有一个名为 {Command('pyproject.toml')} 的文件，其中有上面提到的 [tool.nonebot] 表
{BBPath("bot.py")} 中也存在
{Command('nonebot.load_from_toml("pyproject.toml")')}

此外，还有一个 {Command('load_builtin_plugin')}，用于加载 NoneBot2 内置插件
此函数是对 {Command('load_plugin("nonebot.plugins.x")')} 的包装
导入内置的 echo 插件的代码如下：
{Command('nonebot.load_builtin_plugin("echo")"')}
等同于 {Command('nonebot.load_plugin("nonebot.plugins.echo")')}
目前含有两个内置插件：echo 和 single_session

{Exercise("2-1")}
使用任意方法加载插件 {Command('nonebot_plugin_docs')}（此插件已默认跟随本插件安装）
{Exercise("2-2")}
新建一个文件夹 {BBPath('nblearn_plugins')}，将上一节新建的 {BBPath('hello_nonebot.py')}
和 {BBPath('hello_bot')} 移动到此文件夹，并使用任意方法加载此文件夹的插件
{Exercise("2-3")}
使用任意方法加载内置插件 {Command('echo')}

执行完毕后重启 NoneBot2，发送 “{Command('提交课程2')}” 来提交结果
"""


async def handle_tutorial2(matcher: Matcher, _: MessageEvent):
    img = text2image(TUTORIAL)
    output = BytesIO()
    img.save(output, format="png")
    await matcher.finish(MessageSegment.image(output))


async def commit_tutorial2(matcher: Matcher, _: MessageEvent):
    plugins = get_available_plugin_names()
    error_msgs = []

    # 检查 2-1
    if "nonebot_plugin_docs" not in plugins:
        error_msgs.append("课程2-1未达成条件：未加载插件 nonebot_plugin_docs")
    # 检查 2-2
    error_msgs.extend(check_path(Path("nblearn_plugins"), "课程2-2"))
    if "hello_bot" not in plugins:
        error_msgs.append("课程2-2未达成条件：未加载插件 hello_bot")
    if "hello_nonebot" not in plugins:
        error_msgs.append("课程2-2未达成条件：未加载插件 hello_nonebot")
    if error_msgs:
        await matcher.finish("提交结果失败：\n" + "\n".join(error_msgs))
    else:
        set_state("3")
        await matcher.finish(f"恭喜通过课程2，接下来的课程为：\n{STATES['3']}\n输入命令“课程3”进入")


__tutorial2__ = {"课程2": handle_tutorial2, "提交课程2": commit_tutorial2}
