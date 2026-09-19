#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self, BinaryIO
from abc import ABC, abstractmethod
from functools import partial
from operator import attrgetter
import struct
import argparse
import argcomplete
import write_polys as WP


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
        return self.type_(instance._data[rng])

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


def auto_init(cls):
    fields = [
        key for key in vars(cls).keys() if not (key[:2] == "__" and key[-2:] == "__")
    ]

    def __init__(self, *args):
        super(cls, self).__init__(bytearray(cls._type_size))
        for attr, val in zip(fields, args):
            setattr(self, attr, val)

    cls.__init__ = __init__
    return cls


@auto_init
class Point(View):
    x = "<d"
    y = "<d"


class Box(View):
    p1 = Point
    p2 = Point


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
            yield _factory(self.data[lump])


_POLYS_BIN = ".polys.bin"

parser = argparse.ArgumentParser(
    description="Show .polys.bin file",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("--iter-as", required=1, choices=["<dd", "Point"])


def test_point():
    # p = Point(bytearray(Point._type_size))
    # p.x = 10.1
    # p.y = 20.2
    p = Point(10.1, 20.2)
    assert str(p) == "Point(x=10.1, y=20.2)"


def test_box():
    p1 = Point(bytearray(Point._type_size))
    p1.x = 10.1
    p1.y = 20.2
    b = Box(bytearray(Box._type_size))
    b.p1 = p1
    b.p2 = p1
    assert str(b) == "Box(p1=Point(x=10.1, y=20.2), p2=Point(x=10.1, y=20.2))"


def test_header():
    h0 = WP.Header.default()
    h = Header(bytearray(Header._type_size))
    h.magic = h0.magic
    b0 = h0.box
    p1 = Point(bytearray(Point._type_size))
    p2 = Point(bytearray(Point._type_size))
    p1.x = b0.p1.x
    p1.y = b0.p1.y
    p2.x = b0.p2.x
    p2.y = b0.p2.y
    b = Box(bytearray(Box._type_size))
    b.p1 = p1
    b.p2 = p2
    h.box = b
    h.num_polys = h0.num_polys
    assert (
        str(h)
        == "Header(magic=4660, box=Box(p1=Point(x=0.5, y=0.5), p2=Point(x=7.0, y=9.2)), num_polys=3)"
    )
    # print(h)


if __name__ == "__main__":
    test_header()
# if __name__ == "__main__":
#     argcomplete.autocomplete(parser)
#     args = parser.parse_args()
#     with open(_POLYS_BIN, "rb") as fd:
#         hdr = Header(fd.read(Header._type_size))
#         print(hdr.csv())
#         for _ in range(hdr.num_polys):
#             polys = Sized.from_file(fd)
#             if args.iter_as == "<dd":
#                 for pp in polys.iter_as("<dd"):
#                     print(pp)
#             else:
#                 for pp in polys.iter_as(Point):
#                     print(pp)
