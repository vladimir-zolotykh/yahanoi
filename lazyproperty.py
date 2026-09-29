#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
from types import MethodType
from contextlib import contextmanager
from time import perf_counter
import pytest


class lazyproperty:
    def __init__(self, func: Callable):
        self._func = func
        self.cache_name = ""  # instance cache name
        self.cache = {}  # instance cache dict

    def __call__(self, instance, n, *args, **kwargs):
        print(f"{self = }, {instance = }, {n = }, {args = }, {kwargs = }")
        if n in self.cache:
            return self.cache[n]
        else:
            # val = self._func(n)
            val = MethodType(self._func, instance)(n)
            self.cache[n] = val
            return val

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        self.cache_name = f"_cache_{self._func.__name__}"
        if not getattr(instance, self.cache_name, None):
            setattr(instance, self.cache_name, {})
        return MethodType(self, instance)


@contextmanager
def perf_counter_on(label: str = "perfcounter"):
    start = perf_counter()
    yield
    print("Elapsed: ", perf_counter() - start)


def fib(n):
    if n >= 2:
        return fib(n - 2) + fib(n - 1)
    else:
        return n


class Box:
    @lazyproperty
    def fib(self, n: int) -> int:
        return fib(n)


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


if __name__ == "__main__":
    b = Box()
    print(b.fib(10))
    print(b.fib(20))
