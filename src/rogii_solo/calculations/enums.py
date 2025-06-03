from enum import Enum

from rogii_solo.calculations.exceptions import InvalidMeasureUnitsException


class EMeasureUnits(str, Enum):
    """
    An enumeration representing the measurement unit systems used in the Solo system.
    """

    METER_FOOT = 'METER_FOOT'
    """Mixed unit system using both meters and feet."""

    FOOT = 'FOOT'
    """Imperial unit system using feet."""

    METER = 'METER'
    """Metric unit system using meters."""

    @classmethod
    def includes(cls, value):
        """
        Check if a value is a valid member of the EMeasureUnits enumeration.

        :param value: The value to check.

        :return: True if the value is a valid member, False otherwise.
        """
        return value in cls._value2member_map_


class ELogMeasureUnits(str, Enum):
    """
    An enumeration representing the measurement units used in log data.
    """

    METER = 'm'
    """Metric unit using meters (m)."""

    FOOT = 'ft'
    """Imperial unit using feet (ft)."""

    @classmethod
    def convert_from_measure_units(cls, value: EMeasureUnits):
        """
        Convert a measure unit value to the corresponding log measure unit.

        :param value: The measure unit value to convert.

        :return: The corresponding log measure unit.
        """
        if not EMeasureUnits.includes(value):
            raise InvalidMeasureUnitsException('Invalid measure units value.')

        return cls.METER if value == EMeasureUnits.METER else cls.FOOT
