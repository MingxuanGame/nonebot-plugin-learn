import asyncio
from typing import Union

from nonebot.log import logger
from nonebot.adapters import Bot
from nonebot.message import handle_event
from nonebot import get_driver, on_fullmatch
from nonebot.adapters.onebot.v11 import Message as OBMessage
from nonebot.adapters.console.message import Message as ConsoleMessage
from nonebot.adapters.onebot.v11 import MessageEvent as OBMessageEvent
from nonebot.adapters.console.event import MessageEvent as ConsoleMessageEvent

from .state import get_state

__version__ = "0.1.0"


driver = get_driver()


@driver.on_startup
async def startup():
    logger.opt(colors=True).info(
        f"<green>nonebot-plugin-learn</green> <y>{__version__}</y> 已加载"
    )


def register_tutorial():
    from .tutorial import tutorials

    for k, v in tutorials.items():
        on_fullmatch(k).append_handler(v)
        if "提交" not in k:
            logger.success(f"已加载{k}")


register_tutorial()

matcher = on_fullmatch("当前课程")


@matcher.handle()
async def _(bot: Bot, event: Union[OBMessageEvent, ConsoleMessageEvent]):
    command = f"课程{get_state()}"
    if isinstance(event, OBMessageEvent):
        event.message = OBMessage(command)
        event.original_message = OBMessage(command)
        event.raw_message = command
    else:
        event.message = ConsoleMessage(command)
    asyncio.create_task(handle_event(bot, event))
