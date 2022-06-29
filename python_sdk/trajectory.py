from pandas import DataFrame

from .base import DataFrameable


class TrajectoryPoint(DataFrameable):
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
    def __init__(self, data):
        self._data = data

        super().__init__([TrajectoryPoint(**item) for item in self._data])

    def to_df(self):
        return DataFrame(self._data)

    def find_by_md(self, value):
        return self._find_by_attr(input_list=self, attr='md', value=value)

    def _find_by_attr(self, input_list: list[object], attr: str, value):
        return next((item for item in input_list if getattr(item, attr, None) == value), None)
