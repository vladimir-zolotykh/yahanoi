#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter
import pytest


class TupleMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        super().__init__(cls, bases, clsdict)
        fields = clsdict.get("_fields", [])
        for i, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(i)))


class Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args, **kwargs):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"<class {cls.__name__!r}> gets exactly {n} arguments")
        return super().__new__(cls, args)

    def csv(self):
        return ", ".join(f"{f}={getattr(self, f)!r}" for f in self._fields)


class Person(Tuple):
    _fields = ["name", "age", "salary"]


@pytest.fixture
def bob():
    return Person("Bob", 37, 12000)


def test_person(bob):
    assert str(bob) == "('Bob', 37, 12000)"
    assert (bob.name, bob.age, bob.salary) == ("Bob", 37, 12000)
    assert bob.csv() == "name='Bob', age=37, salary=12000"


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob)
