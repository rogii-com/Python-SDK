from typing import Optional

from pandas import DataFrame

from rogii_solo.base import BaseObject
from rogii_solo.types import DataList


class TrajectoryPoint(BaseObject):
    def __init__(self, **kwargs):
        self.md = None
        self.incl = None
        self.azim = None

        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'md': self.md,
            'incl': self.incl,
            'azim': self.azim,
        }

    def to_df(self):
        return DataFrame([self.to_dict()])


class TrajectoryPointRepository(list):
    def __init__(self, dicts: DataList = None):
        if dicts is None:
            dicts = []

        self._dicts = dicts
        self._objects = [TrajectoryPoint(**item) for item in self._dicts]

        super().__init__(self._objects)

    def to_df(self) -> DataFrame:
        return DataFrame(self._dicts)

    def to_dict(self) -> DataList:
        return self._dicts

    def find_by_md(self, value) -> Optional[TrajectoryPoint]:
        return self._find_by_attr(attr='md', value=value)

    def _find_by_attr(self, attr: str, value) -> Optional[TrajectoryPoint]:
        return next((item for item in self if getattr(item, attr, None) == value), None)
