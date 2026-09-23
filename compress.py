#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


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
