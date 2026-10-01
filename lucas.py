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

    def __copy__(self) -> Self:
        board = Board(*self.pegs)
        return board


def solve(board: Board, n: int, from_: int, to: int, aux: int) -> Board:
    if n <= 0:
        return board
    board = copy(board)
    board = solve(board, n - 1, from_, aux, to)
    move(board, from_, to)
    return solve(board, n - 1, aux, to, from_)


def move(board: Board, from_: int, to: int) -> Board:
    validate(board, from_, to)
    board.pegs[to].append(board.pegs[from_].pop())
    board.num_moves += 1
    return board


def validate(board: Board, from_: int, to: int) -> None:
    if not board.pegs[to]:
        return
    disk: int = board.pegs[from_][-1]
    if disk > (under := board.pegs[to][-1]):
        raise ValueError(f"Cannot put {disk}[{from_}] over {under}[{to}]")


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
        board = Board.from_num_disks(n)
        res = solve(board, n, 0, 2, 1)
        print(res)
