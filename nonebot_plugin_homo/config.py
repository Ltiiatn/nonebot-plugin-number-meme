from __future__ import annotations

from pydantic import BaseModel, Field


class Config(BaseModel):
    """HOMO 数字计算器的插件配置，可在 .env 中通过以下变量覆盖。"""

    homo_max_input: int = Field(
        default=10**12,
        description="允许输入的数字绝对值上限，超过直接拒绝",
    )
    homo_max_length: int = Field(
        default=2000,
        description="生成表达式的最大字符数，超过则认为输入过大",
    )
