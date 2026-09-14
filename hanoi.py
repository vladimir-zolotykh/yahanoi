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


# $ pytest hanoi.py::test_init_peg
@pytest.mark.parametrize(
    "num_disks, peg",
    [
        (1, [1]),
        (2, [2, 1]),
        (3, [3, 2, 1]),
        (4, [4, 3, 2, 1]),
        (5, [5, 4, 3, 2, 1]),
        (6, [6, 5, 4, 3, 2, 1]),
        (7, [7, 6, 5, 4, 3, 2, 1]),
        (8, [8, 7, 6, 5, 4, 3, 2, 1]),
    ],
)
def test_init_peg(num_disks, peg):
    assert init_peg(num_disks) == peg


def evenp(num: int):
    return num % 2 == 0


def oddp(num: int):
    return not evenp(num)


def getaux(peg1, peg2):
    assert peg1 != peg2 and peg1 in (1, 2, 3) and peg2 in (1, 2, 3)
    return 6 - peg1 - peg2


@pytest.mark.parametrize(
    "peg1, peg2, tmp",
    [
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 2, 1),
        (3, 1, 2),
    ],
)
def test_getaux(peg1, peg2, tmp):
    assert getaux(peg1, peg2) == tmp


peg = []


def init_board(num_disks: int):
    global peg

    peg = [None] * 4
    peg[1] = init_peg(num_disks)
    peg[2] = []
    peg[3] = []


def move(peg, src: int, dst: int) -> None:
    peg[dst].append(peg[src].pop())


num_disks = -1


def solve(peg, src: int, dst: int, tmp: int):
    global num_disks
    if num_disks == -1:
        num_disks = len(peg[src])
    if len(dst) == num_disks:
        return
    aux = getaux(src, dst)
    dst, src = src, dst
    solve(peg, src, aux)


def test_solve():
    init_board(3)
    solve(peg, 1, 3)


if __name__ == "__main__":
    test_solve()
    print(peg)
