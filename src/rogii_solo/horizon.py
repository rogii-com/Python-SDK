from typing import Dict, Optional

from pandas import DataFrame

import rogii_solo.interpretation
from rogii_solo.base import BaseObject, ObjectRepository
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.interpretation import (
    get_segments,
    get_segments_boundaries,
    interpolate_horizon,
)
from rogii_solo.calculations.trajectory import calculate_trajectory
from rogii_solo.types import DataList


class Horizon(BaseObject):
    def __init__(self, interpretation: 'rogii_solo.interpretation.Interpretation', **kwargs):
        self.interpretation = interpretation

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

        self._points: Optional[ObjectRepository] = None

    def to_dict(self) -> Dict:
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        return DataFrame([self.to_dict()])

    @property
    def points(self) -> ObjectRepository:
        if self._points is None:
            self._points = ObjectRepository(
                [
                    HorizonPoint(measure_units=self.interpretation.well.project.measure_unit, **point)
                    for point in self._get_points_data()
                ]
            )

        return self._points

    def _get_points_data(self) -> DataList:
        well_data = self.interpretation.well.to_dict(get_converted=False)
        trajectory_data = self.interpretation.well.trajectory.to_dict(get_converted=False)
        assembled_segments_data = self.interpretation.assembled_segments
        measure_units = self.interpretation.well.project.measure_unit

        calculated_trajectory = calculate_trajectory(
            well=well_data, raw_trajectory=trajectory_data, measure_units=measure_units
        )

        segments = get_segments(
            well=well_data,
            assembled_segments=assembled_segments_data['segments'],
            calculated_trajectory=calculated_trajectory,
            measure_units=measure_units,
        )

        segments_boundaries = get_segments_boundaries(
            assembled_segments=segments, calculated_trajectory=calculated_trajectory
        )

        return interpolate_horizon(
            segments_boundaries=segments_boundaries,
            horizon_uuid=self.uuid,
            horizon_tvd=assembled_segments_data['horizons'][self.uuid]['tvd'],
        )


class HorizonPoint(BaseObject):
    def __init__(self, measure_units: EMeasureUnits, md: float, tvd: float) -> None:
        self.measure_units = measure_units
        self.md = md
        self.tvd = tvd

    def to_dict(self, get_converted: bool = True) -> Dict:
        return {
            'md': self.safe_round(self.convert_z(self.md, measure_units=self.measure_units))
            if get_converted
            else self.md,
            'tvd': self.safe_round(self.convert_z(self.tvd, measure_units=self.measure_units))
            if get_converted
            else self.tvd,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])
