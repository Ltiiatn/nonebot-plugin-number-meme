import re
from fractions import Fraction

import pytest

from nonebot_plugin_number_meme.homo import render


def exact_value(expr: str) -> Fraction:
    """用 Fraction 精确求值，避免除法带来的浮点误差。"""
    py = expr.replace("^", "**")
    py = re.sub(r"\d+", lambda m: f"F({m.group()})", py)
    return eval(py, {"F": Fraction}, {})  # noqa: S307


@pytest.mark.parametrize(
    ("num", "expected"),
    [
        (114514, "114514"),
        (400, "-114+514"),
        (0, "(1-1)*4514"),
        (-5, "(11-4-5+1-4)*(11-4*5+14)"),
    ],
)
def test_render_fixed_cases(num: int, expected: str):
    assert render(num) == expected


@pytest.mark.parametrize("num", list(range(-300, 1501)))
def test_render_value_is_correct(num: int):
    """回归测试：表达式算出来的值必须等于输入数字。

    这条测试抓出过 95 个算错的数字（缺括号导致优先级错乱）。
    """
    expr = render(num)
    assert exact_value(expr) == num


@pytest.mark.parametrize("value", ["abc", "", None, True])
def test_invalid_input_returns_empty(value):
    assert render(value) == ""


def test_decimal_input():
    assert render(3.5) == "(11*4+5-14)/(-11/4+51/4)"
