from typing import Any, Dict

from pandas import DataFrame

import rogii_solo.interpretation
from rogii_solo.base import BaseObject
from rogii_solo.calculations.interpretation import get_segments, get_segments_boundaries, interpolate_horizon
from rogii_solo.calculations.trajectory import calculate_trajectory
from rogii_solo.types import Horizon as HorizonType


class Horizon(BaseObject):
    def __init__(self, interpretation: 'rogii_solo.interpretation.Interpretation', **kwargs):
        self.interpretation = interpretation

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return self._get_data(get_converted)

    def to_df(self, get_converted: bool = True) -> HorizonType:
        data = self._get_data(get_converted)

        return {
            'meta': DataFrame([data['meta']]),
            'points': DataFrame(data['points']),
        }

    def _get_data(self, get_converted: bool):
        meta = {
            'uuid': self.uuid,
            'name': self.name,
        }
        points = self._calculate_points(get_converted)

        return {
            'meta': meta,
            'points': points,
        }

    def _calculate_points(self, get_converted: bool):
        well_data = self.interpretation.well.to_dict(get_converted=False)
        trajectory_data = self.interpretation.well.trajectory.to_dict(get_converted=False)
        assembled_segments_data = self.interpretation.assembled_segments
        measure_units = self.interpretation.well.project.measure_unit

        calculated_trajectory = calculate_trajectory(
            well=well_data,
            raw_trajectory=trajectory_data,
            measure_units=measure_units
        )

        segments = get_segments(
            well=well_data,
            assembled_segments=assembled_segments_data['segments'],
            calculated_trajectory=calculated_trajectory,
            measure_units=measure_units
        )

        segments_boundaries = get_segments_boundaries(
            assembled_segments=segments,
            calculated_trajectory=calculated_trajectory
        )

        interpolated_horizon = interpolate_horizon(
            segments_boundaries=segments_boundaries,
            horizon_uuid=self.uuid,
            horizon_tvd=assembled_segments_data['horizons'][self.uuid]['tvd']
        )

        if get_converted:
            return [
                {
                    'md': self.convert_z(point['md'], measure_units=measure_units),
                    'tvd': self.convert_z(point['tvd'], measure_units=measure_units),
                }
                for point in interpolated_horizon
            ]

        return interpolated_horizon
