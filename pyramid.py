#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self
from array import array
import argparse
import pytest
import argcomplete
from copy import copy
from lazyproperty import lazyproperty


class Board:
    def __init__(self, disks: int):
        self.disks = disks
        self.pegs = [array("i", range(disks, 0, -1)), array("i"), array("i")]
        self.moves: int = 0

    @classmethod
    def from_num_disks(cls, num_disks: int) -> Self:
        brd = cls(num_disks)
        brd.disks = num_disks
        brd.pegs = [array("i", range(num_disks, 0, -1)), array("i"), array("i")]
        brd.moves: int = 0
        return brd

    @classmethod
    def from_pegs(cls, *pegs: array, moves: int = 0) -> Self:
        num_disks: int = sum(len(p) for p in pegs)
        brd = cls(num_disks)
        brd.disks = num_disks
        brd.moves = moves
        for i in range(3):
            brd.pegs[i] = copy(pegs[i])
        return brd

    def __copy__(self):
        brd = Board(self.disks)
        for i in range(self.disks):
            brd.pegs[i] = copy(self.pegs[i])
        return brd

    def __repr__(self):
        pegs = ", ".join(str(peg) for peg in self.pegs)
        return f"Board.from_pegs({pegs})"

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

    @lazyproperty
    def solve(self, n: int, from_: int, to: int, aux: int) -> Self:
        if n <= 0:
            return self
        self.solve(n - 1, from_, aux, to)
        self.move(from_, to)
        return self.solve(n - 1, aux, to, from_)


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
    res = board.solve(n, 0, 2, 1)
    assert str(res) == f"[], [], {peg}"
    assert res.moves == total


parser = argparse.ArgumentParser(
    description="Solve Hanoi for [3-8] disks",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
argcomplete.autocomplete(parser)

parser.add_argument(
    "--n",
    type=int,
    nargs="+",
    default=[3],
    choices=list(range(3, 9)),
    help="Number of disks",
)

# Usage: $ python pyramid.py --n 3 4 5
if __name__ == "__main__":
    args = parser.parse_args()
    for n in args.n:
        board = Board(n)
        res = board.solve(n, 0, 2, 1)
        print(res)
