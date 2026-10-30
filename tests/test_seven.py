import re
from fractions import Fraction

import pytest

from nonebot_plugin_number_meme.six_seven import TABLE
from nonebot_plugin_number_meme.six_seven import render


def exact_value(expr: str) -> Fraction:
    """用 Fraction 精确求值，避免 67/6-7/6/7 这类除法带来的浮点误差。"""
    py = expr.replace("^", "**")
    py = re.sub(r"\d+", lambda m: f"F({m.group()})", py)
    return eval(py, {"F": Fraction}, {})  # noqa: S307


@pytest.mark.parametrize(
    ("num", "expected"),
    [
        (13, "67+6+7-67"),
        (42, "67+6*7-67"),
        (67, "67+67-67"),
    ],
)
def test_table_hits_match_original(num: int, expected: str):
    """表内数字直接返回原表达式，不做化简。"""
    assert render(num) == expected


@pytest.mark.parametrize("num", list(range(0, 501)))
def test_render_value_is_correct(num: int):
    """表达式算出来必须精确等于输入。"""
    assert exact_value(render(num)) == num


@pytest.mark.parametrize("num", [3.5, -3.5, 0.25, 0.1, 2.75])
def test_decimal_is_supported(num: float):
    """小数也能表示，且值精确。"""
    assert exact_value(render(num)) == Fraction(str(num))


@pytest.mark.parametrize("num", [3.5, 0.25, Fraction(22, 7), Fraction(1, 3)])
def test_decimal_expression_only_contains_6_and_7(num):
    digits = {char for char in render(num) if char.isdigit()}
    assert digits <= {"6", "7"}


@pytest.mark.parametrize("num", [13, 42, 67, 1000, 12345, 999999])
def test_expression_only_contains_6_and_7(num: int):
    """除运算符外，表达式里只能出现数字 6 和 7。"""
    digits = {char for char in render(num) if char.isdigit()}
    assert digits <= {"6", "7"}


def test_table_is_sorted_descending():
    values = list(TABLE)
    assert values == sorted(values, reverse=True)
