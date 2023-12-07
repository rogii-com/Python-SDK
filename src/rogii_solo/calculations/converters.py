import math
from typing import Optional

from rogii_solo.calculations.constants import FEET_TO_METERS
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.exceptions import InvalidMeasureUnitsException


def convert_value(value: float, measure_units: EMeasureUnits, force_to_meters: bool = False) -> float:
    if not EMeasureUnits.includes(measure_units):
        raise InvalidMeasureUnitsException('Invalid measure units value.')

    if measure_units == EMeasureUnits.METER:
        return value
    elif measure_units == EMeasureUnits.FOOT:
        return meters_to_feet(value)
    elif measure_units == EMeasureUnits.METER_FOOT:
        return value if force_to_meters else meters_to_feet(value)


def meters_to_feet(value: float) -> Optional[float]:
    if value is not None:
        return float(value * (1.0 / FEET_TO_METERS))


def feet_to_meters(value: float) -> Optional[float]:
    if value is not None:
        return float(value * FEET_TO_METERS)


def radians_to_degrees(value: float) -> float:
    return math.degrees(value)


def degrees_to_radians(value: float) -> float:
    return math.radians(value)


def convert_to_meters(value: float, measure_units: EMeasureUnits):
    meters_map = {
        EMeasureUnits.METER: lambda val: value,
        EMeasureUnits.FOOT: lambda val: feet_to_meters(value),
        EMeasureUnits.METER_FOOT: lambda val: feet_to_meters(value),
    }

    return meters_map[measure_units](value)
