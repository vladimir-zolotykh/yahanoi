#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def fib_s(n):
    stack = [(n, False)]
    results = {}

    while stack:
        n, done = stack.pop()

        if n < 2:
            results[n] = n
        elif done:
            results[n] = results[n - 1] + results[n - 2]
        else:
            stack.append((n, True))
            stack.append((n - 2, False))
            stack.append((n - 1, False))

    return results[n]


def fib_r(n):
    if n < 2:
        return n
    else:
        return fib_r(n - 2) + fib_r(n - 1)


fib = fib_r


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
    assert fib(n) == res
