#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class Board:
    peg1 = []
    peg2 = []
    peg3 = []


def init_peg(num_disks):
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


def move(src, dst):
    dst.append(src.pop())


def evenp(num):
    return num % 2 == 0


def oddp(num):
    return not evenp(num)


peg1 = init_peg(3)
peg2 = []
peg3 = []


def solve1():
    move(peg1, peg3)


def solve2():
    move(peg1, peg2)
    move(peg1, peg3)
    move(peg2, peg3)


def solve3():
    move(peg1, peg3)
    move(peg1, peg2)
    move(peg3, peg2)
    move(peg1, peg3)
    move(peg2, peg1)
    move(peg2, peg3)
    move(peg1, peg3)


def solve4():
    move(1, 2)
    move(1, 3)
    move(2, 3)
    move(1, 2)
    move(3, 1)
    move(3, 2)
    move(1, 2)
    move(1, 3)
    move(2, 3)
    move(2, 1)
    move(3, 1)
    move(2, 3)
    move(1, 2)
    move(1, 3)
    move(2, 3)
