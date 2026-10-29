"""通用「数字论证」引擎：一张大表 + 贪心分解。

homo（114514）和 67 共用这套骨架，差别只在数据表和表达式风格：

    1. 表里直接有该数字  → 用表里的表达式
    2. 否则取「表里不大于 n 的最大值 v」，n = q * v + r，递归处理 q 和 r
    3. 最后统一化简多余的括号

第 2 步之所以成立，是因为表里的键全部来自 6/7 或 1/1/4/5/1/4 这类固定数字，
递归到叶子时一定能在表里查到。
"""

from __future__ import annotations

import ast
from bisect import bisect_right
from functools import lru_cache

__all__ = ["GreedyTable", "simplify"]

# ---------------------------------------------------------------------------
# 表达式化简：解析成语法树后按最小括号重新输出
# ---------------------------------------------------------------------------

_PRECEDENCE = {ast.Add: 1, ast.Sub: 1, ast.Mult: 2, ast.Div: 2, ast.Pow: 3}
_SYMBOL = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/", ast.Pow: "^"}
_ATOM = 4
_MUL = _PRECEDENCE[ast.Mult]
_POW = _PRECEDENCE[ast.Pow]


def _rank(node: ast.AST) -> int:
    """节点顶层运算符的优先级。"""
    if isinstance(node, ast.BinOp):
        return _PRECEDENCE.get(type(node.op), _ATOM)
    return _ATOM


def _render_unary(node: ast.UnaryOp) -> str:
    """输出 ``-项``；操作数是加减式时要补括号。"""
    inner = _render(node.operand)
    if _rank(node.operand) < _MUL:
        inner = f"({inner})"
    return "-" + inner


def _render(node: ast.AST) -> str:
    """按运算优先级输出表达式，只在必须的时候加括号。"""
    if isinstance(node, ast.Expression):
        return _render(node.body)

    if isinstance(node, ast.Constant):
        return str(node.value)

    if isinstance(node, ast.UnaryOp):
        return _render_unary(node)

    left = _render(node.left)
    prec = _PRECEDENCE[type(node.op)]

    # 加减一个负数：a+(-b) 写成 a-b，a-(-b) 写成 a+b
    if isinstance(node.op, (ast.Add, ast.Sub)) and isinstance(node.right, ast.UnaryOp):
        inner = _render_unary(node.right)
        joiner = "+" if isinstance(node.op, ast.Sub) else "-"
        return f"{left}{joiner}{inner[1:]}"

    right = _render(node.right)

    # 右操作数本身以负号开头（如 -11+4+14）：a+ 直接并成 a-
    if isinstance(node.op, ast.Add) and right.startswith("-"):
        return left + right

    left_rank, right_rank = _rank(node.left), _rank(node.right)

    wrap_left = left_rank < prec
    if prec == _POW and (left_rank == prec or isinstance(node.left, ast.UnaryOp)):
        wrap_left = True
    if wrap_left:
        left = f"({left})"

    wrap_right = right_rank < prec
    if isinstance(node.op, (ast.Sub, ast.Div)) and right_rank == prec:
        wrap_right = True
    if wrap_right:
        right = f"({right})"

    return f"{left}{_SYMBOL[type(node.op)]}{right}"


def simplify(expr: str) -> str:
    """去掉表达式里多余的括号；解析失败就原样返回。"""
    try:
        tree = ast.parse(expr.replace("^", "**"), mode="eval")
        return _render(tree)
    except (SyntaxError, ValueError, RecursionError, KeyError):
        # 表被改坏时宁可原样返回，也不要让整个插件崩掉
        return expr


# ---------------------------------------------------------------------------
# 贪心引擎
# ---------------------------------------------------------------------------


class GreedyTable:
    """用一张 {数字: 表达式} 表把任意整数改写成该风格的表达式。"""

    def __init__(self, table: dict[int, str]) -> None:
        if not table:
            raise ValueError("数据表不能为空")
        self.table = table
        self._ascending = sorted(table)

    def largest_key_le(self, num: int) -> int:
        """表里不大于 num 的最大键。"""
        index = bisect_right(self._ascending, num) - 1
        if index < 0:
            raise ValueError(f"{num} 小于表中最小的键 {self._ascending[0]}")
        return self._ascending[index]

    def leaf(self, value: int) -> str:
        """把一个键换成表里的表达式（子类可覆盖）。"""
        return self.table[value]

    @lru_cache(maxsize=8192)
    def _build(self, num: int) -> str:
        if num in self.table:
            return f"({self.leaf(num)})"

        divisor = self.largest_key_le(num)
        quotient, remainder = divmod(num, divisor)
        if quotient == 1:
            return f"({self.leaf(divisor)})+({self._build(remainder)})"
        return f"({self.leaf(divisor)})*({self._build(quotient)})+({self._build(remainder)})"

    def render(self, num: int) -> str:
        """返回化简后的最终表达式。"""
        return simplify(self._build(int(num)))
