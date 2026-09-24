import pytest
from compress import count_ones, sum_args


@pytest.mark.parametrize(
    "lst, res",
    [
        ([], 0),
        ([1], 1),
        ([1, 1], 2),
        ([1, 1, 0, 1, 1, 0, 0], 4),
    ],
)
def test_count_ones(lst, res):
    assert count_ones(lst) == res


@pytest.mark.parametrize(
    "args, sum",
    [
        ((), 0),
        ((1,), 1),
        ((1, 2, 3), 6),
    ],
)
def test_sum_args(args, sum):
    assert sum_args(*args) == sum
