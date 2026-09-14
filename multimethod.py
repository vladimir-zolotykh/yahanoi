#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from types import MethodType
from inspect import signature, _empty


class MultiMethod:
    def __init__(self, name):
        self.methods = {}

    def __get__(self, instance, owner=None):
        return MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        key = tuple(type(a) for a in args[1:])
        return self.methods[key](*args, **kwargs)

    def register(self, func):
        sig = signature(func)
        typ = ()
        for name, parm in sig.parameters.items():
            if name == "self":
                continue
            if parm.annotation is _empty:
                raise TypeError(f"{name!r}: no annotation")
            if parm.default is not _empty:
                self.methods[typ] = func
            typ = typ + (parm.annotation,)
        self.methods[typ] = func


class MultiDict(dict):
    def __setitem__(self, key, val):
        mm = self.setdefault(key, MultiMethod())
        mm.register(val)


class MultiMeta(type):
    @classmethod
    def __prepare__(clsname, bases, clsdict):
        return MultiDict()


class Box:
    def add(x: int, y: int) -> int:
        print(f"add-int-int({x}, {y}")
        return x + y

    def add(x: float, y: float = 6.2) -> float:  # noqa: F811
        print(f"add-float-float[6.2]({x}, {y})")
        return x + y

    def add(x: str, y: str) -> str:  # noqa: F811
        print(f"add-str-str({x}, {y})")
        return x + y


def test_multi():
    box = Box()
    box.add(10, 12)
    box.add(7.0, 8.0)
    box.add(7.0)
    box.add("foo", "bar")


if __name__ == "__main__":
    test_multi()
