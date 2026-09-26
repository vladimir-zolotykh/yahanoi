#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import operator
from typeguard import typechecked


class Node:
    pass


class Num(Node):
    @typechecked
    def __init__(self, val: float):
        self.val = val

    def __repr__(self):
        return f"Num({repr(self.val)})"

    # def eval(self) -> float:
    #     return self.val


class Binary(Node):
    def __init__(self, val: str, left: Node, right: Node):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{type(self).__name__}({repr(self.left)}, {repr(self.right)})"

    # def eval(self) -> float:
    #     return self._op(self.left.eval(), self.right.eval())


class Plus(Binary):
    # _op = operator.add

    @typechecked
    def __init__(self, left: Node, right: Node):
        super().__init__("+", left, right)


class Minus(Binary):
    # _op = operator.sub

    def __init__(self, left: Node, right: Node):
        super().__init__("-", left, right)


class Mul(Binary):
    # _op = operator.mul

    def __init__(self, left: Node, right: Node):
        super().__init__("*", left, right)


class Div(Binary):
    # _op = operator.truediv

    def __init__(self, left: Node, right: Node):
        super().__init__("/", left, right)
