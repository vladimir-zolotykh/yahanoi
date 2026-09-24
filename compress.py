#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any
import pytest


def compress(rest, chunk=None, result=[]) -> list[Any]:
    if not rest:
        return result + (chunk[1:] if chunk else [])
    x = rest[0]
    print(f"{chunk = }")
    if chunk:
        if chunk[0] == x:
            chunk[1] += 1
        else:
            if chunk[1] > 1:
                result = result + list(chunk)
            else:
                result = result + list(chunk[0])
                result = result + list(x)
                chunk = None
    else:
        chunk = [x, 1]
    return compress(rest[1:], chunk, result)


def sum_args(*args: int) -> int:
    if not args:
        return 0
    return sum_args(*args[1:]) + args[0]


@pytest.mark.parametrize(
    "args, sum",
    [
        ((), 0),
        ((1,), 1),
        ((1, 2, 3), 6),
    ],
)
def test_sum_args(args, sum):
    assert sum_args(*args) == sum
