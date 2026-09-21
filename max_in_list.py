#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


def max_in_list(lst: list[int]) -> int:
    if len(lst) == 1:
        return lst[0]
    car, cdr = lst[0], lst[1:]
    max = max_in_list(cdr)
    return car if car > max else max


def test_max_in_list():
    lst = [-1, 10, 1, 3, 11, -12, 5]
    assert max_in_list(lst) == 11


def is_palindrome(s: str) -> bool:
    if len(s) == 1:
        return True
    if len(s) == 2:
        return s[0] == s[1]
    return s[0] == s[-1:] and is_palindrome(s[1:-1])


def test_is_palindrome():
    p = "level"
    assert is_palindrome(p)
    p = "A man, a plan, a canal, Panama"
    assert is_palindrome("".join([c.upper() for c in p if c not in (" ", ",")]))


def flatten(lst: list) -> list:
    for x in lst:
        if isinstance(x, list):
            yield from flatten(x)
        else:
            yield x


def sum_digits(num: int) -> int:
    if num < 10:
        return num
    return num % 10 + sum_digits(num // 10)


@pytest.mark.parametrize("num, res", [(9, 9), (19, 10), (199, 19)])
def test_sum_digits(num, res):
    assert sum_digits(num) == res


def test_flatten():
    nested_list = [1, [2, 3], [4, [5, 6], 7], 8]
    flat = list(flatten(nested_list))
    assert flat == [1, 2, 3, 4, 5, 6, 7, 8]


def binary_search(data: list[int], target: int, low: int = -1, high: int = -1):
    if low < 0:
        low = 0
    if high < 0:
        high = len(data)
    if low >= high:
        return low
    mid = (high - low) // 2
    if target == data[mid]:
        return mid
    elif target < data[mid]:
        return binary_search(data, target, low, mid)
    else:
        return binary_search(data, target, mid, high)


def test_binary_search():
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    assert binary_search(data, 5) == 4


if __name__ == "__main__":
    test_max_in_list()
    test_is_palindrome()
    test_flatten()
    test_binary_search()
