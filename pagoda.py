#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Self
from array import array
from copy import copy
import argparse
import argcomplete


class Board:
    def __init__(self, *pegs: array):
        self.pegs = [copy(peg) for peg in pegs]
        self.num_disks = sum(len(peg) for peg in pegs)
        self.num_moves = 0

    def __repr__(self):
        pegs = [str(peg.tolist()) for peg in self.pegs]
        return f"Board({pegs})"

    @classmethod
    def from_num_disks(cls, num_disks: int = 3) -> Self:
        pegs = [array("i", list(range(num_disks, 0, -1))), array("i"), array("i")]
        return cls(*pegs)

    def solve(self, n: int, src: int, dst: int, aux: int):
        if n <= 0:
            return
        self.solve(n - 1, src, aux, dst)
        self.move(src, dst)
        self.solve(n - 1, aux, dst, src)

    def move(self, src: int, dst: int) -> None:
        self.validate(src, dst)
        self.pegs[dst].append(self.pegs[src].pop())
        self.num_moves += 1

    def validate(self, src: int, dst: int) -> None:
        if not self.pegs[dst]:
            return
        disk: int = self.pegs[src][-1]
        if disk > (under := self.pegs[dst][-1]):
            raise ValueError(f"Cannot put {disk}[{src}] over {under}[{dst}]")


parser = argparse.ArgumentParser(
    description="Solve Hanoi for [3-8] disks",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--n",
    type=int,
    nargs="+",
    default=[3],
    choices=list(range(3, 9)),
    help="Number of disks",
)

# Usage: $ python pagoda.py --n 3 4 5
if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    for n in args.n:
        board = Board.from_num_disks(n)
        board.solve(n, 0, 2, 1)
        print(board)
