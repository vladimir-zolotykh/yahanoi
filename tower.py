#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest

pegs = [[], [], []]
pegs[0] = list(range(3, 0, -1))


def validate(from_, to) -> None:
    if not pegs[to]:
        return
    disk = pegs[from_][-1]
    if disk > (under := pegs[to][-1]):
        raise ValueError(f"Cannot put {disk}[{from_}] over {under}[{to}]")


moves: int = 0


def move(from_: int, to: int) -> None:
    global moves
    validate(from_, to)
    pegs[to].append(pegs[from_].pop())
    moves += 1


def init_pegs(n: int = 3):
    global moves
    for i in range(3):
        pegs[i].clear()
    pegs[0] = list(range(n, 0, -1))
    moves = 0


def solve3():
    print(*pegs)
    for from_, to in [
        (0, 2),
        (0, 1),
        (2, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (0, 2),
    ]:
        move(from_, to)
        print(f"{from_}->{to}", "--", *pegs)


def solve8(n, from_, to, aux):
    # print(f"{n = }, {from_ = }, {to = }, {aux = }")
    if n <= 0:
        return
    solve8(n - 1, from_, aux, to)
    move(from_, to)
    solve8(n - 1, aux, to, from_)


@pytest.mark.parametrize(
    "n, peg, total",
    [
        (3, [3, 2, 1], 7),
        (4, [4, 3, 2, 1], 15),
        (5, [5, 4, 3, 2, 1], 31),
    ],
)
def test_solve8(n, peg, total):
    init_pegs(n)
    assert str(pegs) == f"[{peg}, [], []]"
    solve8(n, 0, 2, 1)
    assert str(pegs) == f"[[], [], {peg}]"
    assert moves == total
