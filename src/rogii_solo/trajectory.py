from typing import Any, Dict, Optional

from pandas import DataFrame

from rogii_solo.base import BaseObject
from rogii_solo.types import DataList

well_type = ('rogii_solo.well.Well', 'rogii_solo.typewell.Typewell')


class TrajectoryPoint(BaseObject):
    def __init__(self, well: well_type, **kwargs):
        self.well = well

        self.md = None
        self.incl = None
        self.azim = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.well.project.measure_unit

        return {
            'md': self.convert_z(self.md, measure_units=measure_units) if get_converted else self.md,
            'incl': self.convert_angle(self.incl) if get_converted else self.incl,
            'azim': self.convert_angle(self.azim) if get_converted else self.azim,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])


class TrajectoryPointRepository(list):
    def __init__(self, well: well_type, dicts: DataList = None):
        if dicts is None:
            dicts = []

        self._dicts = dicts
        self._objects = [TrajectoryPoint(well=well, **item) for item in self._dicts]

        super().__init__(self._objects)

    def to_dict(self, get_converted: bool = True) -> DataList:
        if get_converted:
            return [object_.to_dict(get_converted) for object_ in self._objects]

        return self._dicts

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame(self.to_dict(get_converted))

    def find_by_md(self, value) -> Optional[TrajectoryPoint]:
        return self._find_by_attr(attr='md', value=value)

    def _find_by_attr(self, attr: str, value) -> Optional[TrajectoryPoint]:
        return next((item for item in self if getattr(item, attr, None) == value), None)
