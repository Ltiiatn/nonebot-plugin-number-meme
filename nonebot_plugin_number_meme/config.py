from __future__ import annotations

from pydantic import BaseModel, Field


class Config(BaseModel):
    """插件配置，可在 .env 中用 HOMO_* / SEVEN_* 变量覆盖。"""

    homo_max_input: int = Field(
        default=10**12,
        description="「114514 风格」允许输入的绝对值上限",
    )
    homo_max_length: int = Field(
        default=2000,
        description="「114514 风格」生成表达式的最大字符数",
    )
    seven_max_input: int = Field(
        default=10**15,
        description="「67 风格」允许输入的绝对值上限",
    )
    seven_max_length: int = Field(
        default=4000,
        description="「67 风格」生成表达式的最大字符数",
    )
