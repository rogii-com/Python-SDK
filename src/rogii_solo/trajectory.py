from typing import Any, Dict, List, Optional

from pandas import DataFrame

from rogii_solo.base import BaseObject
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.types import DataList


class TrajectoryPoint(BaseObject):
    def __init__(self, measure_units: EMeasureUnits, **kwargs):
        self.measure_units = measure_units

        self.md = None
        self.incl = None
        self.azim = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {
            'md': self.convert_z(self.md, measure_units=self.measure_units) if get_converted else self.md,
            'incl': self.convert_angle(self.incl) if get_converted else self.incl,
            'azim': self.convert_angle(self.azim) if get_converted else self.azim,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])


class TrajectoryPointRepository(list):
    def __init__(self, objects: List[BaseObject] = None):
        if objects is None:
            objects = []

        super().__init__(objects)

    def to_dict(self, get_converted: bool = True) -> DataList:
        return [object_.to_dict(get_converted) for object_ in self]

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame(self.to_dict(get_converted))

    def find_by_md(self, value) -> Optional[TrajectoryPoint]:
        return self._find_by_attr(attr='md', value=value)

    def _find_by_attr(self, attr: str, value) -> Optional[TrajectoryPoint]:
        return next((item for item in self if getattr(item, attr, None) == value), None)
