from pandas import DataFrame

from python_sdk.base import BaseObject, DataFrameable


class NestedWell(BaseObject, DataFrameable):
    def __init__(self, **kwargs):
        self.uuid = None
        self.name = None
        self.xsrf_real = None
        self.ysrf_real = None
        self.kb = None
        self.api = None
        self.operator = None
        self.azimuth = None
        self.convergence = None
        self.tie_in_tvd = None
        self.tie_in_ns = None
        self.tie_in_ew = None

        self.__dict__.update(kwargs)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'xsrf_real': self.xsrf_real,
            'ysrf_real': self.ysrf_real,
            'kb': self.kb,
            'api': self.api,
            'operator': self.operator,
            'azimuth': self.azimuth,
            'convergence': self.convergence,
            'tie_in_tvd': self.tie_in_tvd,
            'tie_in_ns': self.tie_in_ns,
            'tie_in_ew': self.tie_in_ew,
        }

    def to_df(self):
        return DataFrame([self.to_dict()])
