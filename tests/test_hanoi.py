import pytest
from hanoi import init_peg, getaux, init_board, peg, solve


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


@pytest.mark.parametrize("num_disks", (1, 2, 3, 4, 5))
def test_solve(num_disks):
    init_board(peg, num_disks)
    solve(peg, num_disks, 1, 3)
