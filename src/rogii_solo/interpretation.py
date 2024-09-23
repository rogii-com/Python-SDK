from math import fabs
from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.calculations.base import calc_segment_vs_length, get_nearest_values
from rogii_solo.calculations.converters import meters_to_feet
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.trajectory import (
    calculate_trajectory,
    interpolate_trajectory_point,
)
from rogii_solo.calculations.types import HorizonShift, Segment
from rogii_solo.earth_model import EarthModel
from rogii_solo.exceptions import InterpretationOutOfTrajectoryException
from rogii_solo.horizon import Horizon
from rogii_solo.papi.client import PapiClient
from rogii_solo.papi.types import (
    PapiAssembledSegments,
    PapiStarredHorizons,
    PapiTrajectory,
)
from rogii_solo.types import DataList
from rogii_solo.types import Interpretation as InterpretationType

TVT_DATA_MAX_MD_STEP = 100000


class Interpretation(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client)

        self.well = well

        self.uuid = None
        self.name = None
        self.mode = None
        self.owner = None
        self.properties = None
        self.format: Optional[str] = None

        self.__dict__.update(kwargs)

        self._assembled_segments_data: Optional[PapiAssembledSegments] = None
        self._horizons: Optional[ObjectRepository[Horizon]] = None
        self._earth_models: Optional[ObjectRepository[EarthModel]] = None
        self._starred_horizons_data: Optional[PapiStarredHorizons] = None
        self._starred_horizon_top: Optional[Horizon] = None
        self._starred_horizon_center: Optional[Horizon] = None
        self._starred_horizon_bottom: Optional[Horizon] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return self._get_data()

    def to_df(self, get_converted: bool = True) -> InterpretationType:
        data = self._get_data()

        return {
            'meta': DataFrame([data['meta']]),
            'horizons': DataFrame(data['horizons']).transpose(),
            'segments': DataFrame(data['segments']),
            'earth_models': DataFrame(data['earth_models']),
        }

    @property
    def assembled_segments(self):
        if self._assembled_segments_data is not None:
            return self._assembled_segments_data

        self._assembled_segments_data = self._papi_client.get_interpretation_assembled_segments_data(
            interpretation_id=self.uuid
        )

        try:
            well_data = self.well.to_dict(get_converted=False)
            calculated_trajectory = calculate_trajectory(
                raw_trajectory=self.well.trajectory.to_dict(get_converted=False),
                well=well_data,
                measure_units=self.well.project.measure_unit,
            )
            self._assembled_segments_data['segments'] = self._get_fitted_segments(
                calculated_trajectory=calculated_trajectory,
                well=well_data,
                measure_units=self.well.project.measure_unit,
            )
        except InterpretationOutOfTrajectoryException:
            self._assembled_segments_data = None

            return {'horizons': None, 'segments': None}

        assembled_horizons_data = self._assembled_segments_data['horizons']
        measure_units = self.well.project.measure_unit

        for horizon in self.horizons.to_dict():
            assembled_horizons_data[horizon['uuid']]['name'] = horizon['name']

            if measure_units != EMeasureUnits.METER:
                assembled_horizons_data[horizon['uuid']]['tvd'] = meters_to_feet(
                    assembled_horizons_data[horizon['uuid']]['tvd']
                )

        return self._assembled_segments_data

    def get_tvt_data(self, md_step: int = 1) -> DataList:
        return self._papi_client.get_interpretation_tvt_data(interpretation_id=self.uuid, md_step=md_step)

    @property
    def horizons(self) -> ObjectRepository[Horizon]:
        if self._horizons is None:
            self._horizons = ObjectRepository(
                objects=[
                    Horizon(interpretation=self, **item)
                    for item in self._papi_client.get_interpretation_horizons_data(interpretation_id=self.uuid)
                ]
            )

        return self._horizons

    @property
    def earth_models(self) -> ObjectRepository[EarthModel]:
        if self._earth_models is None:
            self._earth_models = ObjectRepository(
                objects=[
                    EarthModel(papi_client=self._papi_client, interpretation=self, **item)
                    for item in self._papi_client.get_interpretation_earth_models_data(interpretation_id=self.uuid)
                ]
            )

        return self._earth_models

    @property
    def starred_horizon_top(self):
        if self._starred_horizon_top is None:
            starred_horizons_data = self._get_starred_horizons_data()
            self._starred_horizon_top = self.horizons.find_by_id(starred_horizons_data['top'])

        return self._starred_horizon_top

    @property
    def starred_horizon_center(self):
        if self._starred_horizon_center is None:
            starred_horizons_data = self._get_starred_horizons_data()
            self._starred_horizon_center = self.horizons.find_by_id(starred_horizons_data['center'])

        return self._starred_horizon_center

    @property
    def starred_horizon_bottom(self):
        if self._starred_horizon_bottom is None:
            starred_horizons_data = self._get_starred_horizons_data()
            self._starred_horizon_bottom = self.horizons.find_by_id(starred_horizons_data['bottom'])

        return self._starred_horizon_bottom

    def _get_data(self):
        meta = {
            'uuid': self.uuid,
            'name': self.name,
            'mode': self.mode,
            'owner': self.owner,
            'format': self.format,
            'properties': self.properties,
        }

        return {
            'meta': meta,
            'horizons': self.assembled_segments['horizons'],
            'segments': self.assembled_segments['segments'],
            'earth_models': self.earth_models,
        }

    def _get_starred_horizons_data(self):
        if self._starred_horizons_data is None:
            self._starred_horizons_data = self._papi_client.get_interpretation_starred_horizons(self.uuid)

        return self._starred_horizons_data

    def _get_fitted_segments(
        self, calculated_trajectory: PapiTrajectory, well: Dict[str, Any], measure_units: EMeasureUnits
    ):
        segments = self._assembled_segments_data['segments']

        if segments is None:
            return

        fitted_segments = []
        min_trajectory_md = calculated_trajectory[0]['md']
        max_trajectory_md = calculated_trajectory[-1]['md']

        if segments[0]['md'] > max_trajectory_md:
            raise InterpretationOutOfTrajectoryException

        for i, segment in enumerate(segments):
            left_segment = segment

            try:
                right_segment = segments[i + 1]
            except IndexError:
                right_segment = None

            if left_segment['md'] < min_trajectory_md or left_segment['md'] > max_trajectory_md:
                continue
            elif right_segment and (left_segment['md'] <= max_trajectory_md < right_segment['md']):
                fitted_segments.append(
                    self._get_truncated_segment(
                        left=left_segment,
                        right=right_segment,
                        well=well,
                        trajectory=calculated_trajectory,
                        measure_units=measure_units,
                    )
                )
            else:
                nearest_points = get_nearest_values(
                    value=left_segment['md'], input_list=calculated_trajectory, key=lambda it: it['md']
                )

                if len(nearest_points) < 2:
                    # Interpretation start MD = calculated trajectory start MD
                    # Otherwise (MD approximately equal or equal the last trajectory point MD) two points are found
                    interpolated_point = calculated_trajectory[0]
                else:
                    nearest_left_point, nearest_right_point = nearest_points
                    interpolated_point = interpolate_trajectory_point(
                        left_point=nearest_left_point,
                        right_point=nearest_right_point,
                        md=left_segment['md'],
                        well=well,
                        measure_units=measure_units,
                    )

                left_segment['vs'] = interpolated_point['vs']
                fitted_segments.append(left_segment)

        return fitted_segments

    def _get_truncated_segment(
        self, left: Segment, right: Segment, well: Dict[str, Any], trajectory: DataList, measure_units: EMeasureUnits
    ) -> Segment:
        new_shifts = {}
        segment_vs_length = calc_segment_vs_length(
            x1=left['x'], y1=left['y'], x2=right['x'], y2=right['y'], azimuth_vs=well['azimuth']
        )
        nearest_points = get_nearest_values(value=left['md'], input_list=trajectory, key=lambda it: it['md'])

        if len(nearest_points) < 2:
            # Interpretation start MD = calculated trajectory start MD
            # Otherwise (MD approximately equal or equal the last trajectory point MD) two points are found
            interpolated_point = trajectory[0]
        else:
            nearest_left_point, nearest_right_point = nearest_points
            interpolated_point = interpolate_trajectory_point(
                left_point=nearest_left_point,
                right_point=nearest_right_point,
                md=left['md'],
                well=well,
                measure_units=measure_units,
            )

        left_point_vs = interpolated_point['vs']
        right_point_vs = trajectory[-1]['vs']

        truncated_segment_vs_length = fabs(right_point_vs - left_point_vs)
        truncated_segment_height = left['end'] - left['start']
        truncated_segment_new_end = (
            truncated_segment_height * truncated_segment_vs_length / segment_vs_length + left['start']
        )

        for uuid, horizons_shift in left['horizon_shifts'].items():
            shift_height = horizons_shift['end'] - horizons_shift['start']
            shift_new_end = shift_height * truncated_segment_vs_length / segment_vs_length + horizons_shift['start']

            new_shifts[uuid] = HorizonShift(
                uuid=horizons_shift['uuid'], start=horizons_shift['start'], end=shift_new_end
            )

        return Segment(
            uuid=left['uuid'],
            md=left['md'],
            x=left['x'],
            y=left['y'],
            vs=left_point_vs,
            boundary_type=left['boundary_type'],
            start=left['start'],
            end=truncated_segment_new_end,
            horizon_shifts=new_shifts,
        )
