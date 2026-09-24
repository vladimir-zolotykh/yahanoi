#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


def print_chunks(lst: list[int], chunk: list[int] = []):
    if not lst:
        if chunk[1] > 1:
            print(chunk)
        else:
            print(chunk[0])
        return
    elt = lst[0]
    if chunk == []:
        chunk = [elt, 1]
    elif chunk[0] == elt:
        chunk[1] += 1
    else:
        if chunk[1] > 1:
            print(chunk)
        else:
            print(chunk[0])
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
