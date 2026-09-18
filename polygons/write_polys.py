#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self
from itertools import chain
import struct
import io

# from typeguard import typechecked

_PolyType = list[tuple[float, float]]
PolysType = list[_PolyType]

POLYS: PolysType = [
    [(1.0, 2.5), (3.5, 4.0), (2.5, 1.5)],
    [(7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0)],
    [(3.4, 6.3), (1.2, 0.5), (4.6, 9.2)],
]


def auto_eq(cls):
    def __eq__(self, other: object) -> bool:
        if isinstance(other, cls):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    cls.__eq__ = __eq__
    return cls


@auto_eq
class Point:
    # @typechecked
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def packed(self):
        return struct.pack("<dd", self.x, self.y)

    @classmethod
    def from_file(cls, f) -> Self:
        return cls(*struct.unpack("<dd", f.read(struct.calcsize("<dd"))))


@auto_eq
class Box:
    # @typechecked
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def packed(self):
        with io.BytesIO() as f:
            f.write(self.p1.packed())
            f.write(self.p2.packed())
            return f.getvalue()

    @classmethod
    def from_file(cls, f) -> Self:
        return cls(Point.from_file(f), Point.from_file(f))


def get_bounding_box(polys: PolysType = POLYS) -> Box:
    return Box(
        Point(min(x for x, _ in chain(*polys)), min(y for _, y in chain(*polys))),
        Point(max(x for x, _ in chain(*polys)), max(y for _, y in chain(*polys))),
    )


@auto_eq
class Header:
    # @typechecked
    def __init__(self, magic: int, box: Box, num_polys: int):
        self.magic = magic
        self.box = box
        self.num_polys = num_polys

    def packed(self) -> bytes:
        with io.BytesIO() as f:
            f.write(struct.pack("<i", self.magic))
            f.write(self.box.packed())
            f.write(struct.pack("<i", self.num_polys))
            return f.getvalue()

    @classmethod
    def default(cls):
        return cls(0x1234, get_bounding_box(POLYS), len(POLYS))

    @classmethod
    def from_file(cls, f) -> Self:
        return cls(
            struct.unpack("<i", f.read(struct.calcsize("<i")))[0],
            Box.from_file(f),
            struct.unpack("<i", f.read(struct.calcsize("<i")))[0],
        )


_POLYS_BIN = ".polys.bin"


def write_polys(filename: str = _POLYS_BIN, polys: PolysType = POLYS):
    header = Header.default()
    with open(filename, "wb") as f:
        f.write(header.packed())
        for poly in polys:
            f.write(struct.pack("<i", len(poly)))
            for point in poly:
                f.write(struct.pack("<dd", *point))


def read_polys(filename: str = _POLYS_BIN) -> PolysType:
    with open(filename, "rb") as f:
        header: Header = Header.from_file(f)
        return [
            [
                struct.unpack("<dd", f.read(struct.calcsize("<dd")))
                for _ in range(num_points)
            ]
            for _ in range(header.num_polys)
            for num_points in [struct.unpack("<i", f.read(struct.calcsize("<i")))[0]]
        ]


if __name__ == "__main__":
    write_polys()
    header = Header.default()
    with open(_POLYS_BIN, "rb") as f:
        header2 = Header.from_file(f)
    assert header == header2
    polys2 = read_polys()
    assert polys2 == POLYS
