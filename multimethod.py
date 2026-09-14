#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from types import MethodType
from functools import wraps
from inspect import signature, _empty


class MultiMethod:
    def __init__(self, name: str = ""):
        self._name = name
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
        if key[:2] == "__" or key[-2:] == "__":
            super().__setitem__(key, val)
        else:
            mm = self.setdefault(key, MultiMethod())
            mm.register(val)


class MultiMeta(type):
    @classmethod
    def __prepare__(clsname, bases, clsdict):
        return MultiDict()


def show_types(func):
    sig = signature(func)
    fname = func.__name__
    for name, parm in sig.parameters.items():
        if name == "self":
            continue
        fname += "-" + parm.annotation.__name__
        if parm.default is not _empty:
            fname += f"[{parm.default}]"

    @wraps(func)
    def wrapper(*args, **kwargs):
        sargs = ", ".join(str(a) for a in args[1:])
        print(f"{fname}({sargs})")
        res = func(*args, **kwargs)
        return res

    return wrapper


class Box(metaclass=MultiMeta):
    @show_types
    def add(self, x: int, y: int) -> int:
        # print(f"add-int-int({x}, {y})")
        return x + y

    @show_types
    def add(self, x: float, y: float = 6.2) -> float:  # noqa: F811
        # print(f"add-float-float[6.2]({x}, {y})")
        return x + y

    @show_types
    def add(self, x: str, y: str) -> str:  # noqa: F811
        # print(f"add-str-str({x!r}, {y!r})")
        return x + y


def test_multi():
    box = Box()
    box.add(10, 12)
    box.add(7.0, 8.0)
    box.add(7.0)
    box.add("foo", "bar")


if __name__ == "__main__":
    test_multi()
