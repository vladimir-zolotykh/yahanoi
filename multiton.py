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
        if cls not in Multiton._instances or key not in Multiton._instances[cls]:
            Multiton._instances[cls] = super().__call__(cls, key, *args, **kwargs)
        return Multiton._instances[cls][key]


class Module(metaclass=Singleton):
    def __init__(self, name: str = "os"):
        self.name = name
        print(f"Initialize Module(name={name})")


class Logger(metaclass=Singleton):
    def __init__(self, name: str = "Init"):
        self.name = name
        print(f"Initialize Logger({name})")


if __name__ == "__main__":
    m1 = Module()
    m2 = Module()
    assert m1 is m2
    g1 = Logger("file")
    g2 = Logger("file")
    assert g1 is g2
