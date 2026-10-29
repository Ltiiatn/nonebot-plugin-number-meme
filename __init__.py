from __future__ import annotations

from collections.abc import Callable

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

from .config import Config
from .homo import render as render_homo
from .six_seven import render as render_seven

__all__ = ["homo", "seven"]

__plugin_meta__ = PluginMetadata(
    name="数字论证计算器",
    description="把数字改写成「114514」或「6/7」风格的等值表达式",
    usage="/homo <数字>   —— 恶臭数字论证\n/67 <数字>     —— Six Seven 风格",
    type="application",
    homepage="https://github.com/Ltiiatn/nonebot-plugin-number-meme",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

config = get_plugin_config(Config)

homo = on_command("homo", aliases={"HOMO"}, priority=10, block=True)
seven = on_command("67", aliases={"six-seven", "sixseven"}, priority=10, block=True)


async def _reply(
    matcher: Matcher,
    text: str,
    render: Callable[[int], str],
    max_input: int,
    max_length: int,
    *,
    allow_float: bool = False,
) -> None:
    """两个命令共用的流程：校验输入 → 生成表达式 → 回复。"""
    if not text:
        await matcher.finish("用法：/<命令> <数字>", at_sender=True)

    try:
        num: int | float = int(text)
    except ValueError:
        if not allow_float:
            await matcher.finish(f"{text!r} 不是整数", at_sender=True)
            return
        try:
            num = float(text)
        except ValueError:
            await matcher.finish(f"{text!r} 不是数字", at_sender=True)
            return

    if abs(num) > max_input:
        await matcher.finish(f"数字太大了，上限是 {max_input}", at_sender=True)

    try:
        expr = render(num)
    except Exception:
        logger.exception(f"处理数字 {num} 失败")
        await matcher.finish("处理失败了，换个数字试试", at_sender=True)

    if not expr:
        await matcher.finish("这个数字处理不了", at_sender=True)

    if len(expr) > max_length:
        await matcher.finish(f"结果太长了（{len(expr)} 字符），换个小点的数字吧", at_sender=True)

    await matcher.finish(f"{text} = {expr}", at_sender=True)


@homo.handle()
async def _(msg: Message = CommandArg()):
    await _reply(
        homo,
        msg.extract_plain_text().strip(),
        render_homo,
        config.homo_max_input,
        config.homo_max_length,
        allow_float=True,
    )


@seven.handle()
async def _(msg: Message = CommandArg()):
    await _reply(
        seven,
        msg.extract_plain_text().strip(),
        render_seven,
        config.seven_max_input,
        config.seven_max_length,
    )
