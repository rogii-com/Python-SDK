from pandas import DataFrame

import rogii_solo.interpretation
from rogii_solo.base import BaseObject
from rogii_solo.calculations.interpretation import get_segments, get_segments_boundaries, interpolate_horizon
from rogii_solo.calculations.trajectory import calculate_trajectory


class Horizon(BaseObject):
    def __init__(self, interpretation: 'rogii_solo.interpretation.Interpretation', **kwargs):
        self.interpretation = interpretation

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

    def to_dict(self):
        return self._get_data()

    def to_df(self):
        data = self._get_data()

        return {
            'meta': DataFrame([data['meta']]),
            'points': DataFrame(data['points']),
        }

    def _get_data(self):
        meta = {
            'uuid': self.uuid,
            'name': self.name,
        }
        points = self._calculate_points()

        return {
            'meta': meta,
            'points': points,
        }

    def _calculate_points(self):
        well_data = self.interpretation.well.to_dict()
        trajectory_data = self.interpretation.well.trajectory.to_dict()
        assembled_segments_data = self.interpretation.assembled_segments_data
        measure_units = self.interpretation.well.project.measure_unit

        calculated_trajectory = calculate_trajectory(
            well=well_data,
            raw_trajectory=trajectory_data,
            measure_unit=measure_units
        )

        segments = get_segments(
            well=well_data,
            assembled_segments=assembled_segments_data['segments'],
            calculated_trajectory=calculated_trajectory,
            measure_unit=measure_units
        )

        segments_boundaries = get_segments_boundaries(
            assembled_segments=segments,
            calculated_trajectory=calculated_trajectory
        )

        return interpolate_horizon(
            segments_boundaries=segments_boundaries,
            horizon_uuid=self.uuid,
            horizon_tvd=assembled_segments_data['horizons'][self.uuid]['tvd']
        )
