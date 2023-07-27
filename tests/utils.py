from typing import Any, Iterable

from numpy import isclose, nan, ndarray

from rogii_solo.calculations.constants import ROUNDING_PRECISION


def np_is_close(a: ndarray | Iterable | float | int, b: ndarray | Iterable | float | int) -> Any:
    if a is None:
        a = nan

    if b is None:
        b = nan

    return isclose(a=a, b=b, rtol=1 / ROUNDING_PRECISION, atol=1 / ROUNDING_PRECISION, equal_nan=True)
