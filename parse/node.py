#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typeguard import typechecked


class Node:
    pass


class Num(Node):
    @typechecked
    def __init__(self, val: float):
        self.val = val

    def __repr__(self):
        return f"Num({repr(self.val)})"


class Binary(Node):
    def __init__(self, val: str, left: Node, right: Node):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{type(self).__name__}({repr(self.left)}, {repr(self.right)})"


class Plus(Binary):
    @typechecked
    def __init__(self, val: str, left: Node, right: Node):
        super().__init__("+", left, right)


class Minus(Binary):
    def __init__(self, val: str, left: Node, right: Node):
        super().__init__("-", left, right)


class Mul(Binary):
    def __init__(self, val: str, left: Node, right: Node):
        super().__init__("*", left, right)


class Div(Binary):
    def __init__(self, val: str, left: Node, right: Node):
        super().__init__("/", left, right)
