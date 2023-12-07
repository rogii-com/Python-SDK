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
            'azimuth': self.safe_round(self.azimuth) if get_converted else self.azimuth,
            'delta_tvd': self.safe_round(self.delta_tvd) if get_converted else self.delta_tvd,
            'delta_vs': self.safe_round(self.delta_vs) if get_converted else self.delta_vs,
            'inclination': self.safe_round(self.inclination) if get_converted else self.inclination,
            'length': self.safe_round(self.length) if get_converted else self.length,
            'origin_base_corridor_tvd': self.safe_round(self.origin_base_corridor_tvd)
            if get_converted
            else self.origin_base_corridor_tvd,
            'origin_md': self.safe_round(self.origin_md) if get_converted else self.origin_md,
            'origin_top_corridor_tvd': self.safe_round(self.origin_top_corridor_tvd)
            if get_converted
            else self.origin_top_corridor_tvd,
            'origin_tvd': self.safe_round(self.origin_tvd) if get_converted else self.origin_tvd,
            'origin_vs': self.safe_round(self.origin_vs) if get_converted else self.origin_vs,
            'origin_x': self.safe_round(self.origin_x) if get_converted else self.origin_x,
            'origin_y': self.safe_round(self.origin_y) if get_converted else self.origin_y,
            'origin_z': self.safe_round(self.origin_z) if get_converted else self.origin_z,
            'target_base_corridor_tvd': self.safe_round(self.target_base_corridor_tvd)
            if get_converted
            else self.target_base_corridor_tvd,
            'target_md': self.safe_round(self.target_md) if get_converted else self.target_md,
            'target_top_corridor_tvd': self.safe_round(self.target_top_corridor_tvd)
            if get_converted
            else self.target_top_corridor_tvd,
            'target_tvd': self.safe_round(self.target_tvd) if get_converted else self.target_tvd,
            'target_vs': self.safe_round(self.target_vs) if get_converted else self.target_vs,
            'target_x': self.safe_round(self.target_x) if get_converted else self.target_x,
            'target_y': self.safe_round(self.target_y) if get_converted else self.target_y,
            'target_z': self.safe_round(self.target_z) if get_converted else self.target_z,
            'tvd_vs': self.safe_round(self.tvd_vs) if get_converted else self.tvd_vs,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])
