#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


def TupleMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        super().__init__(cls, clsname, bases, clsdict)
        fields = clsdict.get("_fields", [])
        for i, name in enumerate(fields):
            setattr(cls, "name", property(itemgetter(i)))


def Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args, **kwargs):
        n = len(cls._fields)
        if len(args) != n:
            raise TypeError(f"<class {cls.__name__!r}>: gets exactly {n} arguments")
        return super().__new__(cls, args)


class Exercise(Tuple):
    _fields = ["name", "weight", "reps"]


def test_tuple():
    e = Exercise("squat", 77.5, 2)
    print(e)


if __name__ == "__main__":
    test_tuple()
