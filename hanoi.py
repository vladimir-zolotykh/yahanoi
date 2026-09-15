#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typeguard import typechecked

_PegType = list[int]
PegsType = list[_PegType]


class Board:
    peg1: _PegType = []
    peg2: _PegType = []
    peg3: _PegType = []


def init_peg(num_disks: int) -> _PegType:
    return list(range(num_disks, 0, -1))


def evenp(num: int) -> bool:
    return num % 2 == 0


def oddp(num: int) -> bool:
    return not evenp(num)


def getaux(peg1, peg2):
    assert peg1 != peg2 and peg1 in (1, 2, 3) and peg2 in (1, 2, 3)
    return 6 - peg1 - peg2


peg: PegsType = [[0]] * 4


@typechecked
def init_board(pegs: PegsType, disks: int) -> None:
    pegs[1] = init_peg(disks)
    pegs[2] = []
    pegs[3] = []


@typechecked
def move(peg: PegsType, src: int, dst: int) -> None:
    try:
        assert peg[dst][-1] > peg[src][-1]
    except IndexError:
        pass
    peg[dst].append(peg[src].pop())


@typechecked
def solve(peg: PegsType, num_disks: int, src: int, dst: int) -> None:
    if num_disks == 1:
        move(peg, 1, 3)
        assert len(peg[3]) == num_disks
    elif num_disks == 2:
        move(peg, 1, 2)
        move(peg, 1, 3)
        move(peg, 2, 3)
        assert len(peg[3]) == num_disks
    elif num_disks == 3:
        move(peg, 1, 3)
        move(peg, 1, 2)
        move(peg, 3, 2)
        move(peg, 1, 3)
        move(peg, 2, 1)
        move(peg, 2, 3)
        move(peg, 1, 3)
        assert len(peg[3]) == num_disks
    elif num_disks == 4:
        move(peg, 1, 2)
        move(peg, 1, 3)
        move(peg, 2, 3)
        move(peg, 1, 2)
        move(peg, 3, 1)
        move(peg, 3, 2)
        move(peg, 1, 2)
        move(peg, 1, 3)
        move(peg, 2, 3)
        move(peg, 2, 1)
        move(peg, 3, 1)
        move(peg, 2, 3)
        move(peg, 1, 2)
        move(peg, 1, 3)
        move(peg, 2, 3)
        assert len(peg[3]) == num_disks


if __name__ == "__main__":
    num_disks = 3
    init_board(peg, num_disks)
    solve(peg, num_disks, 1, 3)
    print(peg)
