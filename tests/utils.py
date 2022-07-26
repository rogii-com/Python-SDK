from typing import Any, Iterable
from numpy import isclose, ndarray

from rogii_solo.calculations.constants import DELTA


def np_is_close(a: ndarray | Iterable | float | int, b: ndarray | Iterable | float | int) -> Any:
    return isclose(a=a, b=b, rtol=DELTA)
