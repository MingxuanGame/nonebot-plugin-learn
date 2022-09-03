from pathlib import Path

from nonebot import get_driver
from nonebot.matcher import Matcher
from nonebot.adapters.console.event import MessageEvent
from nonebot.adapters.console.message import MessageSegment

TUTORIAL = (Path(__file__).parent / "tutorial.md").read_text(encoding="utf-8")


async def handle_tutorial0(matcher: Matcher, _: MessageEvent):
    config = get_driver().config
    host = config.host
    port = config.port
    await matcher.finish(
        MessageSegment.markdown(TUTORIAL.format(host=host, port=port))
    )


__chapter0__ = {"课程0": handle_tutorial0}
