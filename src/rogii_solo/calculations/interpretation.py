from math import fabs
from typing import Any, Dict, List

from rogii_solo.calculations.base import (
    calc_segment_dip,
    find_by_md,
    find_last_by_md,
    get_most_common,
    get_nearest_values,
    interpolate_linear
)
from rogii_solo.calculations.constants import DELTA
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.trajectory import interpolate_trajectory_point
from rogii_solo.calculations.types import (
    AssembledHorizons,
    Segment,
    SegmentBoundaries,
    SegmentsBoundaries,
    SegmentWithDip,
    Trajectory
)
from rogii_solo.papi.types import PapiAssembledSegments


def get_segments(
        well: Dict[str, Any],
        calculated_trajectory: Trajectory,
        assembled_segments: PapiAssembledSegments,
        measure_units: EMeasureUnits
) -> List[Segment]:
    segments = []
    mds, mds_map = [], {}

    for i, point in enumerate(calculated_trajectory):
        mds.append(point['md'])
        mds_map[point['md']] = i

    for assembled_segment in assembled_segments:
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
                measure_units=measure_units,
            )

        segments.append(Segment(
            md=assembled_segment['md'],
            vs=interpolated_point['vs'],
            start=assembled_segment['start'],
            end=assembled_segment['end'],
            horizon_shifts=assembled_segment['horizon_shifts'],
        ))

    last_trajectory_point = calculated_trajectory[-1]
    segments.append(Segment(
        md=last_trajectory_point['md'],
        vs=last_trajectory_point['vs'],
        start=None,
        end=None,
        horizon_shifts=segments[-1]['horizon_shifts'],
    ))

    return segments


def get_segments_with_dip(
        segments: List[Segment],
        assembled_horizons: AssembledHorizons
) -> List[SegmentWithDip]:
    segments_with_dip = [
        SegmentWithDip(**segment, dip=None) for segment in segments
    ]

    for i in range(len(segments) - 1):
        left_point = segments[i]
        right_point = segments[i + 1]

        if len(assembled_horizons):
            segment_dips = []
            sorted_assembled_horizons = {
                uuid: assembled_horizon
                for uuid, assembled_horizon in sorted(
                    assembled_horizons.items(),
                    key=lambda horizon_: horizon_[1]['tvd']
                )
            }

            for horizon_uuid, horizon in sorted_assembled_horizons.items():
                if fabs(right_point['md'] - left_point['md']) < DELTA:
                    segment_dip = None
                    segment_dips.append(segment_dip)
                    continue

                horizon_shifts = left_point['horizon_shifts'][horizon_uuid]
                shift_start = horizon_shifts['start']
                shift_end = horizon_shifts['end']

                segment_dip = calc_segment_dip(
                    delta_x=fabs(right_point['vs'] - left_point['vs']),
                    delta_y=shift_end - shift_start
                )
                segment_dips.append(segment_dip)

            result_dip = get_most_common(segment_dips)
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


def get_segments_boundaries(assembled_segments: List[Segment], calculated_trajectory) -> SegmentsBoundaries:
    segments_boundaries = []
    segments_mds = [segment['md'] for segment in assembled_segments]
    calculated_trajectory_last_point_md = calculated_trajectory[-1]['md']

    for calculated_trajectory_point in calculated_trajectory:
        calculated_point_md = calculated_trajectory_point['md']
        nearest_segments_mds = get_nearest_values(value=calculated_point_md, input_list=segments_mds)

        if len(nearest_segments_mds) < 2:
            segment_md = nearest_segments_mds[0]

            if calculated_point_md < segment_md:
                segments_boundaries.append(
                    SegmentBoundaries(
                        md=calculated_point_md,
                        left_point=None,
                        right_point=None,
                        interpolated_point=calculated_trajectory_point
                    )
                )
                continue
            else:
                left_point_md = segment_md
                right_point_md = calculated_trajectory_last_point_md
        else:
            left_point_md, right_point_md = nearest_segments_mds

        left_point = find_last_by_md(left_point_md, assembled_segments)
        right_point = find_by_md(right_point_md, assembled_segments)

        segments_boundaries.append(
            SegmentBoundaries(
                md=calculated_point_md,
                left_point=left_point,
                right_point=right_point,
                interpolated_point=calculated_trajectory_point
            )
        )

    return segments_boundaries


def interpolate_horizon(segments_boundaries: SegmentsBoundaries, horizon_uuid: str, horizon_tvd: float):
    points = []

    for segment_boundaries in segments_boundaries:
        md = segment_boundaries['md']
        left_point = segment_boundaries['left_point']
        right_point = segment_boundaries['right_point']
        interpolated_point = segment_boundaries['interpolated_point']

        if left_point is None:
            points.append({
                'md': md,
                'tvd': None
            })
            continue

        horizon_shift_start = left_point['horizon_shifts'][horizon_uuid]['start']
        horizon_shift_end = left_point['horizon_shifts'][horizon_uuid]['end']

        left_point_tvd = horizon_tvd + horizon_shift_start
        right_point_tvd = horizon_tvd + horizon_shift_end

        tvd = interpolate_linear(
            x0=left_point['vs'],
            y0=left_point_tvd,
            x1=right_point['vs'],
            y1=right_point_tvd,
            x=interpolated_point['vs']
        )

        points.append({
            'md': md,
            'tvd': tvd
        })

    return points
