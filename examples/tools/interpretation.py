from math import fabs
from typing import List

from pandas import DataFrame

from .base import calc_segment_dip, get_nearest_values, get_most_common

from .trajectory import interpolate_trajectory_point
from .constants import DELTA
from .enums import EMeasureUnits


def _calc_segments_dip(segments: List, assembled_horizons: DataFrame):
    segments_with_dip = segments.copy()
    horizons = assembled_horizons.transpose().to_dict()

    for i in range(len(segments) - 1):
        left_point = segments[i]
        right_point = segments[i + 1]

        if len(horizons):
            segment_horizon_dips = []
            sorted_assembled_horizons = dict(
                sorted(horizons.items(), key=lambda _horizon: _horizon[1]['tvd'])
            )

            for horizon_uuid, horizon in sorted_assembled_horizons.items():
                if fabs(right_point['md'] - left_point['md']) < DELTA:
                    segment_dip = None
                    segment_horizon_dips.append(segment_dip)
                    continue

                horizon_shifts = left_point['horizon_shifts'][horizon_uuid]
                shift_start = horizon_shifts['start']
                shift_end = horizon_shifts['end']

                segment_dip = calc_segment_dip(
                    delta_x=fabs(right_point['vs'] - left_point['vs']),
                    delta_y=shift_end - shift_start
                )
                segment_horizon_dips.append(segment_dip)

            result_dip = get_most_common(segment_horizon_dips)
        else:
            shift_start = left_point['start']
            shift_end = left_point['end']

            result_dip = calc_segment_dip(
                delta_x=fabs(right_point['vs'] - left_point['vs']),
                delta_y=shift_end - shift_start
            )

        segments_with_dip[i]['dip'] = result_dip

    if len(segments) > 0:
        segments_with_dip[-1]['dip'] = (
            90 if len(segments) == 1
            else segments_with_dip[-2]['dip']
        )

    return segments_with_dip


def get_segments(
        well: dict,
        assembled_segments: DataFrame,
        assembled_horizons: DataFrame,
        calculated_trajectory: List,
        measure_unit: EMeasureUnits
):
    mds, mds_map = [], {}
    for i, point in enumerate(calculated_trajectory):
        mds.append(point['md'])
        mds_map[point['md']] = i

    segments = []
    for i, assembled_segment in assembled_segments.iterrows():
        nearest_mds = get_nearest_values(
            value=assembled_segment['md'],
            input_list=mds
        )

        if len(nearest_mds) < 2:
            # Interpretation start MD = calculated trajectory start MD
            # Otherwise (MD approximately equal or equal the last trajectory point MD) two points are found
            interpolated_point = calculated_trajectory[0]
        else:
            left_point_md, right_point_md = nearest_mds

            left_point = calculated_trajectory[mds_map[left_point_md]]
            right_point = calculated_trajectory[mds_map[right_point_md]]

            interpolated_point = interpolate_trajectory_point(
                left_point=left_point,
                right_point=right_point,
                md=assembled_segment['md'],
                well=well,
                measure_unit=measure_unit,
            )

        segments.append(dict(
            md=assembled_segment['md'],
            vs=interpolated_point['vs'],
            start=assembled_segment['start'],
            end=assembled_segment['end'],
            horizon_shifts=assembled_segment['horizon_shifts'],
        ))

    last_trajectory_point = calculated_trajectory[-1]
    segments.append(dict(
        md=last_trajectory_point['md'],
        vs=last_trajectory_point['vs'],
        horizon_shifts=segments[-1]['horizon_shifts'],
    ))

    return _calc_segments_dip(segments=segments, assembled_horizons=assembled_horizons)
