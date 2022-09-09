from enum import Enum


class EMeasureUnits(str, Enum):
    METER_FOOT = 'METER_FOOT'
    FOOT = 'FOOT'
    METER = 'METER'

    @classmethod
    def includes(cls, value):
        return value in cls._value2member_map_
