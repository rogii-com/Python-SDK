from typing import Dict, List, Optional

from pandas import DataFrame

from .base import BaseObject


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


class TrajectoryPointList(list):
    def __init__(self, dict_list: List[Dict]):
        self._dict_list = dict_list

        super().__init__([TrajectoryPoint(**item) for item in self._dict_list])

    def to_df(self) -> DataFrame:
        return DataFrame(self._dict_list)

    def to_dict(self) -> List[Dict]:
        return self._dict_list

    def find_by_md(self, value) -> Optional[TrajectoryPoint]:
        return self._find_by_attr(attr='md', value=value)

    def _find_by_attr(self, attr: str, value) -> Optional[TrajectoryPoint]:
        return next((item for item in self if getattr(item, attr, None) == value), None)
