#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self
from array import array
import pytest


class Board:
    def __init__(self, disks: int):
        self.pegs = [array("i", range(disks, 0, -1)), array("i"), array("i")]
        self.moves: int = 0

    def __str__(self):
        return ", ".join(str(a.tolist()) for a in self.pegs)

    def validate(self, from_: int, to: int) -> None:
        if not self.pegs[to]:
            return
        disk: int = self.pegs[from_][-1]
        if disk > (under := self.pegs[to][-1]):
            raise ValueError(f"Cannot put {disk}[{from_}] over {under}[{to}]")

    def move(self, from_: int, to: int) -> Self:
        self.validate(from_, to)
        self.pegs[to].append(self.pegs[from_].pop())
        self.moves += 1
        return self

    def solve(self, n: int, from_: int, to: int, aux: int) -> Self:
        if n <= 0:
            return Self
        self.solve(n - 1, from_, aux, to)
        self.move(from_, to)
        self.solve(n - 1, aux, to, from_)


@pytest.mark.parametrize(
    "n, peg, total",
    [
        (3, [3, 2, 1], 7),
        (4, [4, 3, 2, 1], 15),
        (5, [5, 4, 3, 2, 1], 31),
        (6, [6, 5, 4, 3, 2, 1], 63),
        (7, [7, 6, 5, 4, 3, 2, 1], 127),
        (8, [8, 7, 6, 5, 4, 3, 2, 1], 255),
    ],
)
def test_solve(n, peg, total):
    board = Board(n)
    assert str(board) == f"{peg}, [], []"
    board.solve(n, 0, 2, 1)
    assert str(board) == f"[], [], {peg}"
    assert board.moves == total
