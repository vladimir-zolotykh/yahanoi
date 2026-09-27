#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

pegs = [[], [], []]
pegs[0] = list(range(3, 0, -1))


def validate(from_, to) -> None:
    if not pegs[to]:
        return
    disk = pegs[from_][-1]
    if disk > (under := pegs[to][-1]):
        raise ValueError(f"Cannot put {disk}[{from_}] over {under}[{to}]")


def move(from_: int, to: int) -> None:
    validate(from_, to)
    pegs[to].append(pegs[from_].pop())


def init_pegs():
    for i in range(3):
        pegs[i].clear()
    pegs[0] = list(range(3, 0, -1))


def solve3():
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
        print(f"move({from_}, {to}) -- {pegs}")
