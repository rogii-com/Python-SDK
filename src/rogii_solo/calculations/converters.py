import math

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


def meters_to_feet(value: float) -> float:
    return float(value * (1.0 / FEET_TO_METERS))


def feet_to_meters(value: float) -> float:
    return float(value * FEET_TO_METERS)


def radians_to_degrees(value: float) -> float:
    return math.degrees(value)


def degrees_to_radians(value: float) -> float:
    return math.radians(value)


METERS_MAP = {
    EMeasureUnits.METER: lambda value: value,
    EMeasureUnits.FOOT: lambda value: feet_to_meters(value),
    EMeasureUnits.METER_FOOT: lambda value: feet_to_meters(value)
}


def convert_to_meters(value: float, measure_units: EMeasureUnits):
    return METERS_MAP[measure_units](value)
