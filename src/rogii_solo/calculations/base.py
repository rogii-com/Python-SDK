import math
from bisect import bisect_left
from collections import Counter
from typing import Any, Dict, List, Optional

from rogii_solo.calculations.constants import DELTA


def calc_hypotenuse_length(cathetus1: float, cathetus2: float) -> Optional[float]:
    if cathetus1 is None or cathetus2 is None:
        return

    return math.sqrt(
        math.pow(cathetus1, 2) +
        math.pow(cathetus2, 2)
    )


def calc_atan2(y: float, x: float) -> Optional[float]:
    if x is None or y is None:
        return

    return math.atan2(y, x) or 0


def calc_vs(angle: float, distance: float, direction: float) -> Optional[float]:
    if any(arg is None for arg in (angle, distance, direction)):
        return

    return distance * math.cos(angle - direction)


def calc_shape_factor(dog_leg: float) -> Optional[float]:
    if dog_leg is None:
        return

    if (
        math.fabs(dog_leg) > DELTA and
        math.fabs(dog_leg - math.pi) > DELTA
    ):
        return 2.0 * math.tan(0.5 * dog_leg) / dog_leg

    return 1.0


def normalize_angle(angle: float) -> float:
    if not angle:
        return 0.0

    modified_angle = angle

    while modified_angle < 0:
        modified_angle += 2 * math.pi

    while modified_angle > 2 * math.pi:
        modified_angle -= 2 * math.pi

    return modified_angle


def get_nearest_values(value: Any, input_list: List[Any]) -> Any:
    if not input_list:
        return

    pos = bisect_left(input_list, value)

    if pos == 0:
        values = [input_list[0]]
    elif pos == len(input_list):
        values = [input_list[-1]]
    else:
        values = [
            input_list[pos - 1],
            input_list[pos]
        ]

    return values


def interpolate_linear(x0: float, y0: float, x1: float, y1: float, x: float) -> Optional[float]:
    if any(arg is None for arg in (x0, y0, x1, y1, x)):
        return

    if x0 == x1:
        return y0

    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def calc_segment_dip(delta_x: float, delta_y: float) -> Optional[float]:
    if (
            delta_x is None or
            delta_y is None or
            delta_x < DELTA
    ):
        return

    angle = math.atan2(delta_y, delta_x)

    return 90 - math.degrees(angle)


def get_most_common(input_list: List[Any]) -> Any:
    if not input_list:
        return

    return Counter(input_list).most_common()[0][0]


def find_by_key(key: str, value: float, input_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    return next((item for item in input_list if item[key] == value), {})


def find_last_by_key(key: str, value: float, input_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    filtered_list = [item for item in input_list if item[key] == value]
    return filtered_list[-1] if len(filtered_list) > 0 else {}


def find_by_md(value: float, input_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    return find_by_key('md', value, input_list)


def find_last_by_md(value: float, input_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    return find_last_by_key('md', value, input_list)
