#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instances:
            Singleton._instances[cls] = super().__call__(*args, **kwargs)
        return Singleton._instances[cls]


class Multiton(type):
    pass


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
