import pytest
from compress import count_ones, sum_args, cat


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


@pytest.mark.parametrize(
    "lst, chunk, res",
    [
        ([], [], []),
        (None, None, []),
        ([1, 0], None, [1, 0]),
        ([1, 1, 1], 3, [1, 1, 1, 3]),
        ([1, 1, 1], [3], [1, 1, 1, [3]]),
        ([1, 1, 1], [3, 3], [1, 1, 1, [3, 3]]),
    ],
)
def test_cat(lst, chunk, res):
    assert cat(lst, chunk) == res
