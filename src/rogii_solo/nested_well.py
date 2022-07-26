from typing import Any, Dict

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, Convertable


class NestedWell(BaseObject, Convertable):
    def __init__(self, well: 'rogii_solo.well.Well', **kwargs):
        self.well = well

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

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.well.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'xsrf_real': self.xsrf_real,
            'ysrf_real': self.ysrf_real,
            'kb': self.convert_z(self.kb, measure_units=measure_units) if get_converted else self.kb,
            'api': self.api,
            'operator': self.operator,
            'azimuth': self.convert_angle(self.azimuth) if get_converted else self.azimuth,
            'convergence': self.convert_angle(self.convergence) if get_converted else self.convergence,
            'tie_in_tvd': self.tie_in_tvd,
            'tie_in_ns': self.tie_in_ns,
            'tie_in_ew': self.tie_in_ew,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])
