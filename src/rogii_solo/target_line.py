from typing import Any, Dict

from pandas import DataFrame

from rogii_solo.base import BaseObject


class TargetLine(BaseObject):
    def __init__(self, **kwargs):
        self.uuid = None
        self.name = None
        self.azimuth = None
        self.delta_tvd = None
        self.delta_vs = None
        self.inclination = None
        self.length = None
        self.origin_base_corridor_tvd = None
        self.origin_md = None
        self.origin_top_corridor_tvd = None
        self.origin_tvd = None
        self.origin_vs = None
        self.origin_x = None
        self.origin_y = None
        self.origin_z = None
        self.target_base_corridor_tvd = None
        self.target_md = None
        self.target_top_corridor_tvd = None
        self.target_tvd = None
        self.target_vs = None
        self.target_x = None
        self.target_y = None
        self.target_z = None
        self.tvd_vs = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'name': self.name,
            'azimuth': self.azimuth,
            'delta_tvd': self.delta_tvd,
            'delta_vs': self.delta_vs,
            'inclination': self.inclination,
            'length': self.length,
            'origin_base_corridor_tvd': self.origin_base_corridor_tvd,
            'origin_md': self.origin_md,
            'origin_top_corridor_tvd': self.origin_top_corridor_tvd,
            'origin_tvd': self.origin_tvd,
            'origin_vs': self.origin_vs,
            'origin_x': self.origin_x,
            'origin_y': self.origin_y,
            'origin_z': self.origin_z,
            'target_base_corridor_tvd': self.target_base_corridor_tvd,
            'target_md': self.target_md,
            'target_top_corridor_tvd': self.target_top_corridor_tvd,
            'target_tvd': self.target_tvd,
            'target_vs': self.target_vs,
            'target_x': self.target_x,
            'target_y': self.target_y,
            'target_z': self.target_z,
            'tvd_vs': self.tvd_vs,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])
