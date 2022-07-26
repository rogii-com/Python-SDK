from typing import Any, Iterable
from numpy import isclose, ndarray, nan

from rogii_solo.calculations.constants import DELTA


def np_is_close(a: ndarray | Iterable | float | int, b: ndarray | Iterable | float | int) -> Any:
    if a is None:
        a = nan

    if b is None:
        b = nan

    return isclose(a=a, b=b, rtol=DELTA, equal_nan=True)
