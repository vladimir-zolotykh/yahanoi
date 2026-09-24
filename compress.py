#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def cat(lst, chunk):
    if not lst and not chunk:
        return []
    if lst and not chunk:
        return lst
    if lst and chunk:
        return lst + [chunk]


def replace_chunks(lst, chunk=[], res=[]):
    if not lst:
        return cat(res, chunk)
    if not chunk:
        chunk = [None, 0]
    x = lst[0]
    if chunk[0] == x:
        chunk[1] += 1
        return replace_chunks(lst[1:], chunk, res)
    else:
        return replace_chunks(lst[1:], None, cat(res, chunk))


@pytest.mark.parametrize(
    "lst, chunk, res, expected",
    [
        ([], [], [], []),
    ],
)
def test_replace_chunks(lst, chunk, res, expected):
    assert replace_chunks(lst, chunk, res) == expected


def count_ones(lst: list[int], count: int = 0) -> int:
    if not lst:
        return count
    if lst[0] == 1:
        count += 1
    return count_ones(lst[1:], count)


def sum_args(*args: int) -> int:
    if not args:
        return 0
    return sum_args(*args[1:]) + args[0]
