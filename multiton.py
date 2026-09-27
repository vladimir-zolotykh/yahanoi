#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


def _get_key(*args, **kwargs):
    return args + tuple(sorted([f"{k}={v}" for k, v in kwargs.items()]))


class Cached(type):
    _cache = defaultdict(dict)

    def __call__(cls, *args, **kwargs):
        cache = type(cls)._cache
        key = _get_key(*args, **kwargs)
        if cls not in cache or key not in cache[cls]:
            cache[cls][key] = super().__call__(*args, **kwargs)
        return cache[cls][key]


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        instances = type(cls)._instances
        if cls not in instances:
            instances[cls] = super().__call__(*args, **kwargs)
        return instances[cls]


class Multiton(type):
    _instances = defaultdict(dict)

    def __call__(cls, key, *args, **kwargs):
        instances = type(cls)._instances
        if cls not in instances or key not in instances[cls]:
            instances[cls][key] = super().__call__(key, *args, **kwargs)
        return instances[cls][key]


class Module(metaclass=Singleton):
    def __init__(self, name: str = "os"):
        self.name = name
        print(f"Initialize Module(name={name})")


class Logger(metaclass=Singleton):
    def __init__(self, name: str = "Init"):
        self.name = name
        print(f"Initialize Logger({name})")


class Connection(metaclass=Multiton):
    def __init__(self, key):
        self.key = key
        print(f"Initialize Connection({key})")


class Person(metaclass=Cached):
    def __init__(self, name, age, salary):
        print(f"Initialize Person({name}, {age}, {salary})")
        self.name = name
        self.age = age
        self.salary = salary


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    assert Person("Bob", 37, 12000) is bob
    bob2 = Person("Bob", 38, 12000)

    c1 = Connection("Vista")
    c2 = Connection("Vista")
    assert c1 is c2
    m1 = Module()
    m2 = Module()
    assert m1 is m2
    g1 = Logger("file")
    g2 = Logger("file")
    assert g1 is g2
