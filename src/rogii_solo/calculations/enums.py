from enum import Enum

from rogii_solo.calculations.exceptions import InvalidMeasureUnitsException


class EMeasureUnits(str, Enum):
    METER_FOOT = 'METER_FOOT'
    FOOT = 'FOOT'
    METER = 'METER'

    @classmethod
    def includes(cls, value):
        return value in cls._value2member_map_


class ELogMeasureUnits(str, Enum):
    METER = 'm'
    FOOT = 'ft'

    @classmethod
    def convert_from_measure_units(cls, value: EMeasureUnits):
        if not EMeasureUnits.includes(value):
            raise InvalidMeasureUnitsException('Invalid measure units value.')

        return cls.METER if value == EMeasureUnits.METER else cls.FOOT
