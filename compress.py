#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import getitem, setitem
import pytest


class NamedList(list):
    def __init__(self, names, values):
        super().__init__(values)
        for i, name in enumerate(names):
            setattr(
                self.__class__,
                name,
                property(
                    lambda self, i=i: getitem(self, i),
                    lambda self, val, i=i: setitem(self, i, val),
                ),
            )


class Chunk(NamedList):
    def __init__(self, cnt: int, val: int):
        super().__init__(("cnt", "val"), (cnt, val))


def jchunk1(all_chunks: list[int | Chunk], chunk: Chunk):
    # if chunk[0] > 1:
    if chunk.cnt > 1:
        return all_chunks + [chunk]
    else:
        # return all_chunks + [chunk[1]]
        return all_chunks + [chunk.val]


def join_chunks(
    lst: list[int], chunk: list[int] = [], all_chunks: list[int | list[int]] = []
):
    if not lst:
        return jchunk1(all_chunks, chunk)
    elt = lst[0]
    if chunk == []:
        # chunk = [1, elt]
        chunk = Chunk(1, elt)
    elif chunk[1] == elt:
        # chunk[0] += 1
        chunk.cnt += 1
    else:
        all_chunks = jchunk1(all_chunks, chunk)
        # chunk = [1, elt]
        chunk = Chunk(1, elt)
    return join_chunks(lst[1:], chunk, all_chunks)


@pytest.mark.parametrize(
    "lst, chunk, all_chunks, expected",
    [
        ([1, 1, 1, 0, 1, 0, 0, 0], [], [], [[3, 1], 0, 1, [3, 0]]),
        ([1, 1, 1, 0, 1, 0, 0, 0, 0], [], [], [[3, 1], 0, 1, [4, 0]]),
    ],
)
def test_join_chunks(lst, chunk, all_chunks, expected):
    assert join_chunks(lst, chunk, all_chunks) == expected


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
