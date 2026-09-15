#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class Board:
    peg1 = []
    peg2 = []
    peg3 = []


def init_peg(num_disks: int):
    return list(range(num_disks, 0, -1))


def evenp(num: int):
    return num % 2 == 0


def oddp(num: int):
    return not evenp(num)


def getaux(peg1, peg2):
    assert peg1 != peg2 and peg1 in (1, 2, 3) and peg2 in (1, 2, 3)
    return 6 - peg1 - peg2


peg = [None] * 4


def init_board(disks: int):
    peg[1] = init_peg(disks)
    peg[2] = []
    peg[3] = []


def move(peg, src: int, dst: int) -> None:
    try:
        assert peg[dst][-1] > peg[src][-1]
    except IndexError:
        pass
    peg[dst].append(peg[src].pop())


def solve(peg, num_disks: int, src: int, dst: int):
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
    init_board(num_disks)
    solve(peg, num_disks, 1, 3)
    print(peg)
