#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import wraps
from contextlib import contextmanager
from time import perf_counter
import argparse
import argcomplete


@contextmanager
def perf_counter_on(label: str = "perfcounter"):
    start = perf_counter()
    yield
    print("{:s} elapsed: {:.2f}".format(label, perf_counter() - start))


def fibcache(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = tuple(args) + tuple(sorted(f"{k}={v}" for k, v in kwargs.items()))
        if key in cache:
            res = cache[key]
        else:
            res = func(*args, **kwargs)
            cache[key] = res
        return res

    return wrapper


@fibcache
def fib(n):
    if n >= 2:
        return fib(n - 2) + fib(n - 1)
    else:
        return n


parser = argparse.ArgumentParser(
    description="Cache Fibonacci results",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("--n", type=int, nargs="+", default=[5])
parser.add_argument("--cache-off", action="store_true")
argcomplete.autocomplete(parser)
if __name__ == "__main__":
    args = parser.parse_args()
    for n in args.n:
        with perf_counter_on(f"fib({n})"):
            if args.cache_off:
                print("Cache is off")
                fib = fib.__wrapped__
                res = fib(n)
            else:
                res = fib(n)
        print(f"{res = }")
