#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self, BinaryIO, TypeVar
from abc import ABC, abstractmethod
from functools import partial
from operator import attrgetter
import struct
import argparse
import argcomplete

T = TypeVar("T")
# import write_polys as WP


def init_as(init_type: type, real_type: type[T], data: memoryview | bytes) -> T:
    """Create real_type class, init it as init_type"""
    obj = real_type.__new__(real_type)
    init_type.__init__(obj, data)
    return obj


class Field(ABC):
    def __init__(self, name: str, off: int):
        self._name = name
        self.off = off

    def __get__(self, instance, owner=None):
        return self.fetch(instance)

    def __set__(self, instance, value):
        self.drop(instance, value)

    @abstractmethod
    def fetch(self, instance):
        pass

    @abstractmethod
    def drop(self, instance):
        pass


class FieldStr(Field):
    def __init__(self, name: str, off: int, format: str):
        super().__init__(name, off)
        self.fmt = format

    def fetch(self, instance):
        rng = slice(self.off, self.off + struct.calcsize(self.fmt))
        t = struct.unpack_from(self.fmt, instance._data[rng])
        return t[0] if len(t) == 1 else t

    def drop(self, instance, val):
        rng = slice(self.off, self.off + struct.calcsize(self.fmt))
        instance._data[rng] = struct.pack(self.fmt, val)


class FieldType(Field):
    def __init__(self, name: str, off: int, type_: type):
        super().__init__(name, off)
        self.type_ = type_

    def fetch(self, instance):
        rng = slice(self.off, self.off + self.type_._type_size)
        obj = init_as(View, self.type_, instance._data[rng])
        return obj

    def drop(self, instance, val):
        rng = slice(self.off, self.off + self.type_._type_size)
        instance._data[rng] = val._data


class FieldMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        off = 0
        fields = []
        for key, val in clsdict.items():
            if key[:2] == "__" and key[-2:] == "__":
                continue
            if isinstance(val, str):
                clsdict[key] = FieldStr(key, off, val)
                off += struct.calcsize(val)
                fields.append(key)
            elif isinstance(val, type):
                clsdict[key] = FieldType(key, off, val)
                off += val._type_size
                fields.append(key)
            else:
                continue
        clsdict["_fields"] = fields
        clsdict["_type_size"] = off

        return super().__new__(mcls, clsname, bases, clsdict)


class View(metaclass=FieldMeta):
    def __init__(self, bytesdata: bytes | memoryview):
        self._data = memoryview(bytesdata)

    def csv(self):
        return ", ".join(f"{key}={getattr(self, key)!r}" for key in self._fields)

    def __repr__(self):
        return f"{type(self).__name__}({self.csv()})"

    @classmethod
    def from_args(cls, *args) -> Self:
        obj = cls(bytearray(cls._type_size))
        keys = [
            key
            for key in vars(cls).keys()
            if not (key[:2] == "__" and key[-2:] == "__")
        ]
        for key, val in zip(keys, args):
            setattr(obj, key, val)
        return obj


def auto_init(cls):
    fields = [
        key for key in vars(cls).keys() if not (key[:2] == "__" and key[-2:] == "__")
    ]

    def __init__(self, *args):
        super(cls, self).__init__(bytearray(cls._type_size))
        for key, val in zip(fields, args):
            setattr(self, key, val)

    cls.__init__ = __init__
    return cls


@auto_init
class Point(View):
    x = "<d"
    y = "<d"


@auto_init
class Box(View):
    p1 = Point
    p2 = Point


@auto_init
class Header(View):
    magic = "<i"
    box = Box
    num_polys = "<i"


class Sized:
    def __init__(self, data: bytes | memoryview):
        self.data = memoryview(data)

    @classmethod
    def from_file(cls, f: BinaryIO) -> Self:
        (size,) = struct.unpack("<i", f.read(struct.calcsize("<i")))
        return cls(f.read(size * struct.calcsize("<dd")))

    def iter_as(self, fmt_or_type):
        _size, _factory = (
            (struct.calcsize, partial(struct.unpack_from, fmt_or_type))
            if isinstance(fmt_or_type, str)
            else (attrgetter("_type_size"), fmt_or_type)
        )
        for off in range(0, len(self.data), _size(fmt_or_type)):
            lump = slice(off, off + _size(fmt_or_type))
            if isinstance(_factory, type):
                obj = init_as(View, _factory, self.data[lump])
                yield obj
            else:
                yield _factory(self.data[lump])


_POLYS_BIN = ".polys.bin"

parser = argparse.ArgumentParser(
    description="Show .polys.bin file",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("--iter-as", required=1, choices=["<dd", "Point"])


if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with open(_POLYS_BIN, "rb") as fd:
        hdr = init_as(View, Header, fd.read(Header._type_size))
        print(hdr.csv())
        for _ in range(hdr.num_polys):
            polys = Sized.from_file(fd)
            if args.iter_as == "<dd":
                for pp in polys.iter_as("<dd"):
                    print(pp)
            else:
                for pp in polys.iter_as(Point):
                    print(pp)
