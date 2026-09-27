#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


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


if __name__ == "__main__":
    c1 = Connection("Vista")
    c2 = Connection("Vista")
    assert c1 is c2
    m1 = Module()
    m2 = Module()
    assert m1 is m2
    g1 = Logger("file")
    g2 = Logger("file")
    assert g1 is g2
