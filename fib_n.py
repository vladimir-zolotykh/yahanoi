#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class Node:
    def __init__(self, val: int):
        self.val = val

    def __repr__(self):
        return f"N({self.val})"

    def eval(self) -> int:
        return self.val


class Plus(Node):
    def __init__(self, n1: int, n2: int):
        self.n1 = n1
        self.n2 = n2

    def __repr__(self):
        return f"P({self.n1}, {self.n2})"

    def eval(self):
        return self.n1.eval() + self.n2.eval()


def fib_n(n: int) -> Node:
    if n < 2:
        return Node(n)
    else:
        return Plus(fib_n(n - 2), fib_n(n - 1))


@pytest.mark.parametrize(
    "n, res",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
    ],
)
def test_fib(n, res):
    assert fib_n(n).eval() == res


if __name__ == "__main__":
    node = fib_n(4)
    print(node)
    print(node.eval())
