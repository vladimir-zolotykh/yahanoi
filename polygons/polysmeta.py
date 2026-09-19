#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self, BinaryIO
from abc import ABC, abstractmethod
import struct


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
        instance._data[rng] = struct.pack(self.fmt, val)  # ???


class FieldType(Field):
    def __init__(self, name: str, off: int, type_: type):
        super().__init__(name, off)
        self.type_ = type_

    def fetch(self, instance):
        rng = slice(self.off, self.off + self.type_._type_size)
        return self.type_(instance._data[rng])

    def drop(self, instance, val):
        rng = slice(self.off, self.off + self.type_._type_size)
        instance._data[rng] = val  # ???


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
        if isinstance(fmt_or_type, str):
            for off in range(0, len(self.data), struct.calcsize(fmt_or_type)):
                lump = slice(off, off + struct.calcsize(fmt_or_type))
                yield struct.unpack_from(fmt_or_type, self.data[lump])
        elif isinstance(fmt_or_type, type):
            for off in range(0, len(self.data), fmt_or_type._type_size):
                lump = slice(off, off + fmt_or_type._type_size)
                yield fmt_or_type(self.data[lump])


_POLYS_BIN = ".polys.bin"

if __name__ == "__main__":
    with open(_POLYS_BIN, "rb") as fd:
        hdr = Header(fd.read(Header._type_size))
        print(hdr.csv())
        for _ in range(hdr.num_polys):
            polys = Sized.from_file(fd)
            # for pp in polys.iter_as("<dd"):
            #     print(pp)
            for pp in polys.iter_as(Point):
                print(pp)
