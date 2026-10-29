from __future__ import annotations

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

from . import homo_generator
from .config import Config

__all__ = ["homo"]

__plugin_meta__ = PluginMetadata(
    name="HOMO 数字计算器",
    description="把数字转换成「114514 风格」的四则运算表达式",
    usage="/homo <数字>\n别名：/HOMO",
    type="application",
    homepage="https://github.com/Ltiiatn/nonebot-plugin-homo",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

config = get_plugin_config(Config)

homo = on_command("homo", aliases={"HOMO"}, priority=10, block=True)


@homo.handle()
async def _(msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if not text:
        await homo.finish("用法：/homo <数字>", at_sender=True)

    try:
        num = int(text)
    except ValueError:
        await homo.finish(f"{text!r} 不是整数", at_sender=True)
        return

    if abs(num) > config.homo_max_input:
        await homo.finish(f"数字太大了，上限是 {config.homo_max_input}", at_sender=True)

    try:
        expr = homo_generator.finisher(homo_generator.demolish(num))
    except Exception:
        logger.exception(f"homo: 处理 {text!r} 失败")
        await homo.finish("处理失败了，换个数字试试", at_sender=True)
        return

    if len(expr) > config.homo_max_length:
        await homo.finish(f"结果太长了（{len(expr)} 字符），换个小点的数字吧", at_sender=True)
        return

    await homo.finish(f"{text} = {expr}", at_sender=True)
