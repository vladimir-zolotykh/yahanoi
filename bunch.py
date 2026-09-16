#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class BunchMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        defaults = {}

        def init(self, **kwargs):
            for key, val in defaults.items():
                setattr(self, key, kwargs[key] if key in kwargs else val)

        def repr(self):
            csv = ", ".join(
                f"{key}={val2}"
                for key, val in defaults.items()
                if (val2 := getattr(self, key)) != val
            )
            return f"{type(self).__name__}({csv})"

        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                if key in ("__init__", "__repr__"):
                    raise TypeError(f"Cannot overwrite {key!r}")
                continue
            defaults[key] = val
        clsdict["__slots__"] = ["name", "age", "pension"]
        clsdict["__init__"] = init
        clsdict["__repr__"] = repr
        return super().__new__(mcls, clsname, bases, clsdict)


class Person(metaclass=BunchMeta):
    name = "Vladimir"
    age = 61
    pension = 4606.93


def test_person():
    p = Person()
    print(p)


if __name__ == "__main__":
    test_person()
