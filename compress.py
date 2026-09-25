#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def jchunk1(all_chunks, chunk):
    if chunk[1] > 1:
        return all_chunks + [chunk]
    else:
        return all_chunks + [chunk[0]]


def join_chunks(
    lst: list[int], chunk: list[int] = [], all_chunks: list[int | list[int]] = []
):
    if not lst:
        return jchunk1(all_chunks, chunk)
    elt = lst[0]
    if chunk == []:
        chunk = [elt, 1]
    elif chunk[0] == elt:
        chunk[1] += 1
    else:
        all_chunks = jchunk1(all_chunks, chunk)
        chunk = [elt, 1]
    return join_chunks(lst[1:], chunk, all_chunks)


@pytest.mark.parametrize(
    "lst, chunk, all_chunks, expected",
    [
        ([1, 1, 1, 0, 1, 0, 0, 0], [], [], [[1, 3], 0, 1, [0, 3]]),
    ],
)
def test_join_chunks(lst, chunk, all_chunks, expected):
    join_chunks(lst, chunk, all_chunks) == expected


def pchunk1(chunk):
    if chunk[1] > 1:
        print(chunk)
    else:
        print(chunk[0])


def print_chunks(lst: list[int], chunk: list[int] = []):
    if not lst:
        pchunk1(chunk)
        return
    elt = lst[0]
    if chunk == []:
        chunk = [elt, 1]
    elif chunk[0] == elt:
        chunk[1] += 1
    else:
        pchunk1(chunk)
        chunk = [elt, 1]
    print_chunks(lst[1:], chunk)


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
