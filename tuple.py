#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter
import pytest


class TupleMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        fields = clsdict.get("_fields", [])
        for i, name in enumerate(fields):
            setattr(cls, "name", property(itemgetter(i)))


class Tuple(tuple, metaclass=TupleMeta):
    _fields: list[str] = []

    def __new__(cls, *args, **kwargs):
        n = len(cls._fields)
        if len(args) != n:
            raise TypeError(f"<class {cls.__name__!r}>: gets exactly {n} arguments")
        return super().__new__(cls, args)


class Exercise(Tuple):
    _fields = ["name", "weight", "reps"]


def test_tuple():
    e = Exercise("squat", 77.5, 2)
    assert str(e) == "('squat', 77.5, 2)"
    with pytest.raises(TypeError, match="<class 'Exercise'>: gets exactly 3 arguments"):
        Exercise("squat", 77.5)
    with pytest.raises(TypeError, match="<class 'Exercise'>: gets exactly 3 arguments"):
        Exercise("squat", 77.5, 3, "failed")


if __name__ == "__main__":
    test_tuple()
