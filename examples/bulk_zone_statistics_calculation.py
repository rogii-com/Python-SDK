from os import environ
from typing import Any, Dict, List, Optional, Tuple

from numpy import arange, ndarray

from rogii_solo import SoloClient
from rogii_solo.calculations.base import calc_hypotenuse_length, get_nearest_values
from rogii_solo.calculations.converters import feet_to_meters, radians_to_degrees
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.interpretation import get_segments
from rogii_solo.calculations.trajectory import (
    calculate_trajectory,
    interpolate_trajectory_point,
)
from rogii_solo.calculations.types import Trajectory, TrajectoryPoint
from rogii_solo.horizon import Horizon
from rogii_solo.interpretation import Interpretation
from rogii_solo.well import Well

STEP_LENGTH = 1
MAX_STEP_NUMBER = 50
# Inclination for start MD range, degrees
LANDING_INCLINATION = 75
DELTA = 0.000001


def restrict_trajectory(trajectory: Trajectory, start_md: float) -> Trajectory:
    index = next((index for index, item in enumerate(trajectory) if item['md'] > start_md), None)
    return trajectory[index:]


def get_segment_range(start_md: float, end_md: float, default_segment_step: float) -> ndarray:
    segment_length = end_md - start_md
    step_number = min(segment_length // default_segment_step, MAX_STEP_NUMBER)
    md_step = segment_length / step_number

    # Function doesn't return the start_md as a part of the array.
    # end_md must be in the returned range, so use: end_md + md_step
    return arange(start_md + md_step, end_md + md_step, md_step, dtype=float)


def interpolate_trajectory(
    well_data: Dict[str, Any], trajectory: Trajectory, measure_units: EMeasureUnits
) -> Trajectory:
    interpolated_trajectory = [trajectory[0]]
    step = feet_to_meters(STEP_LENGTH) if measure_units != EMeasureUnits.METER else STEP_LENGTH

    for i in range(len(trajectory) - 1):
        segment_range = get_segment_range(trajectory[i]['md'], trajectory[i + 1]['md'], step)

        for md in segment_range:
            interpolated_point = interpolate_trajectory_point(
                left_point=trajectory[i],
                right_point=trajectory[i + 1],
                md=md,
                well=well_data,
                measure_units=EMeasureUnits.METER,
            )
            interpolated_trajectory.append(interpolated_point)

    return interpolated_trajectory


def insert_points_in_trajectory(
    well_data: Dict[str, Any], trajectory: Trajectory, point_mds: List[float], measure_units: EMeasureUnits
):
    for point_md in point_mds:
        mds, mds_map = [], {}

        for i, point in enumerate(trajectory):
            mds.append(point['md'])
            mds_map[point['md']] = i

        nearest_mds = get_nearest_values(value=point_md, input_list=mds)

        left_point_md, right_point_md = nearest_mds
        left_point = trajectory[mds_map[left_point_md]]
        right_point = trajectory[mds_map[right_point_md]]

        interpolated_point = interpolate_trajectory_point(
            left_point=left_point,
            right_point=right_point,
            md=point_md,
            well=well_data,
            measure_units=measure_units,
        )

        trajectory.insert(mds_map[right_point_md], interpolated_point)


def calculate_segment_vs_tvds(
    segments: List[Dict[str, Any]], assembled_segments_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    for i, segment in enumerate(segments):
        if i < len(segments) - 1:
            segment['end_md'] = segments[i + 1]['md']

            for horizon_shift in segment['horizon_shifts'].values():
                horizon_tvd = assembled_segments_data['horizons'][horizon_shift['uuid']]['tvd']
                horizon_shift['start_vs'] = segment['vs']
                horizon_shift['start_tvd'] = horizon_tvd + horizon_shift['start']
                horizon_shift['end_vs'] = segments[i + 1]['vs']
                horizon_shift['end_tvd'] = horizon_tvd + horizon_shift['end']

    # Remove pseudo-segment with last trajectory point
    del segments[-1]

    return segments


def get_horizons_and_landing_md(
    well: Well,
    calculated_trajectory: Any,
    top_horizon_name: str,
    base_horizon_name: str,
    landing_point_topset_name: str,
    landing_point_top_name: str,
) -> Tuple[Interpretation, Horizon, Horizon, float]:
    interpretation = well.starred_interpretation

    if not interpretation:
        raise Exception(f'Starred interpretation in the well "{well.name}" not found.')

    top_horizon = (
        interpretation.horizons.find_by_name(top_horizon_name)
        if top_horizon_name
        else interpretation.starred_horizon_top.name
    )

    if not top_horizon:
        raise Exception(
            f'Top of zone in the interpretation "{interpretation.name}" in the well "{well.name}" not found.'
        )

    base_horizon = (
        interpretation.horizons.find_by_name(base_horizon_name)
        if base_horizon_name
        else interpretation.starred_horizon_bottom.name
    )

    if not base_horizon:
        raise Exception(
            f'Bottom of zone in the interpretation "{interpretation.name}" in the well "{well.name}" not found.'
        )

    landing_md: float = 0.0

    if landing_point_topset_name and landing_point_top_name:
        topset = well.topsets.find_by_name(landing_point_topset_name)
        top = topset.tops.find_by_name(landing_point_top_name)
        landing_md = top.md
    else:
        for point in calculated_trajectory:
            if radians_to_degrees(point['incl']) >= LANDING_INCLINATION:
                landing_md = point['md']
                break

    if not landing_md:
        raise Exception(f'Landing point not found for the well "{well.name}".')

    assembled_segments = interpretation.assembled_segments['segments']
    interpretation_start_md = assembled_segments[0]['md']
    landing_md = max(landing_md, interpretation_start_md)

    return interpretation, top_horizon, base_horizon, landing_md


def in_polygon(
    point_x: float,
    point_y: float,
    top_horizon_start_x: float,
    top_horizon_start_y: float,
    top_horizon_end_x: float,
    top_horizon_end_y: float,
    base_horizon_start_x: float,
    base_horizon_start_y: float,
    base_horizon_end_x: float,
    base_horizon_end_y: float,
) -> bool:
    xp = []
    yp = []
    xp.append(top_horizon_start_x)
    xp.append(top_horizon_end_x)
    xp.append(base_horizon_end_x)
    xp.append(base_horizon_start_x)
    yp.append(top_horizon_start_y)
    yp.append(top_horizon_end_y)
    yp.append(base_horizon_end_y)
    yp.append(base_horizon_start_y)
    result = 0

    for i in range(len(xp)):
        if ((yp[i] <= point_y < yp[i - 1]) or (yp[i - 1] <= point_y < yp[i])) and (
            point_x > (xp[i - 1] - xp[i]) * (point_y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i]
        ):
            result = 1 - result

    return bool(result)


def is_point_inside_horizons_shifts(
    point: TrajectoryPoint, top_horizon_shift: Dict[str, Any], base_horizon_shift: Dict[str, Any]
) -> bool:
    return in_polygon(
        point_x=point['vs'],
        point_y=point['tvd'],
        top_horizon_start_x=top_horizon_shift['start_vs'],
        top_horizon_start_y=top_horizon_shift['start_tvd'],
        top_horizon_end_x=top_horizon_shift['end_vs'],
        top_horizon_end_y=top_horizon_shift['end_tvd'],
        base_horizon_start_x=base_horizon_shift['start_vs'],
        base_horizon_start_y=base_horizon_shift['start_tvd'],
        base_horizon_end_x=base_horizon_shift['end_vs'],
        base_horizon_end_y=base_horizon_shift['end_tvd'],
    )


def calculate_lines_intersection(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    x4: float,
    y4: float,
    find_outside_segment: bool = False,
) -> Tuple[Optional[float], Optional[float]]:
    # Check if none of the lines are of length 0
    if (x1 == x2 and y1 == y2) or (x3 == x4 and y3 == y4):
        return None, None

    denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

    #  Lines are parallel
    if denominator == 0:
        return None, None

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator

    #  Is the intersection along the segments
    if (ua < 0 or ua > 1 or ub < 0 or ub > 1) and not find_outside_segment:
        return None, None

    #  Return an object with the x and y coordinates of the intersection
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)

    return x, y


def calculate_intersection_points_with_horizon(
    point: TrajectoryPoint, right_point: TrajectoryPoint, top_horizon: Dict[str, Any]
):
    vs, tvd = calculate_lines_intersection(
        point['vs'],
        point['tvd'],
        right_point['vs'],
        right_point['tvd'],
        top_horizon['start_vs'],
        top_horizon['start_tvd'],
        top_horizon['end_vs'],
        top_horizon['end_tvd'],
    )

    return {'vs': vs, 'tvd': tvd}


def is_in_segment(segment: Dict[str, Any], left_point: TrajectoryPoint, right_point: TrajectoryPoint) -> bool:
    return (
        segment['md'] <= left_point['md'] <= segment['end_md']
        and segment['md'] <= right_point['md'] <= segment['end_md']
    )


def get_length_in_piece(
    left_point: TrajectoryPoint,
    right_point: TrajectoryPoint,
    segment: Dict[str, Any],
    top_horizon_uuid: str,
    base_horizon_uuid: str,
):
    top_horizon = segment['horizon_shifts'][top_horizon_uuid]
    base_horizon = segment['horizon_shifts'][base_horizon_uuid]
    left_point_inside = is_point_inside_horizons_shifts(
        point=left_point, top_horizon_shift=top_horizon, base_horizon_shift=base_horizon
    )
    right_point_inside = is_point_inside_horizons_shifts(
        point=right_point, top_horizon_shift=top_horizon, base_horizon_shift=base_horizon
    )

    if not left_point_inside and not right_point_inside:
        return 0

    if left_point_inside and right_point_inside:
        return right_point['md'] - left_point['md']

    # Calculate intersected part of piece

    top_point = calculate_intersection_points_with_horizon(left_point, right_point, top_horizon)
    base_point = calculate_intersection_points_with_horizon(left_point, right_point, base_horizon)

    if left_point_inside and not right_point_inside:
        start_point = top_point if top_point['vs'] is not None else base_point
        end_point = {'vs': left_point['vs'], 'tvd': left_point['tvd']}
    elif not left_point_inside and right_point_inside:
        start_point = top_point if top_point['vs'] is not None else base_point
        end_point = {'vs': right_point['vs'], 'tvd': right_point['tvd']}
    else:
        start_point = top_point
        end_point = base_point

    return calc_hypotenuse_length(end_point['vs'] - start_point['vs'], end_point['tvd'] - start_point['tvd'])


def calc_zone_statistics(
    well: Well,
    calculated_trajectory: Any,
    top_horizon_name: str,
    base_horizon_name: str,
    landing_point_topset: str,
    landing_point_top: str,
    measure_units: EMeasureUnits,
) -> Dict[str, float]:
    interpretation, top_horizon, base_horizon, landing_md = get_horizons_and_landing_md(
        well=well,
        calculated_trajectory=calculated_trajectory,
        top_horizon_name=top_horizon_name,
        base_horizon_name=base_horizon_name,
        landing_point_topset_name=landing_point_topset,
        landing_point_top_name=landing_point_top,
    )

    well_data = well.to_dict(get_converted=False)

    assembled_segments_data = interpretation.assembled_segments
    segments = get_segments(
        well=well_data,
        assembled_segments=assembled_segments_data['segments'],
        calculated_trajectory=calculated_trajectory,
        measure_units=measure_units,
    )
    tvds_segments = calculate_segment_vs_tvds(segments, assembled_segments_data)

    zone_start_md = max(landing_md, tvds_segments[0]['md'])

    interpolated_trajectory = interpolate_trajectory(
        well_data=well_data, trajectory=calculated_trajectory, measure_units=measure_units
    )

    point_mds = [segment['md'] for segment in tvds_segments]
    point_mds.append(zone_start_md)
    insert_points_in_trajectory(
        well_data=well_data, trajectory=interpolated_trajectory, point_mds=point_mds, measure_units=measure_units
    )

    restricted_trajectory = restrict_trajectory(trajectory=calculated_trajectory, start_md=zone_start_md - DELTA)

    total_length = restricted_trajectory[-1]['md'] - restricted_trajectory[0]['md']
    in_zone_length = 0

    for point_index, point in enumerate(restricted_trajectory):
        if point_index < len(restricted_trajectory) - 1:
            segment_index = next(
                (
                    index
                    for index, segment in enumerate(tvds_segments)
                    if is_in_segment(segment, point, restricted_trajectory[point_index + 1])
                ),
                None,
            )

            if segment_index is None:
                continue

            in_zone_length += get_length_in_piece(
                left_point=point,
                right_point=restricted_trajectory[point_index + 1],
                segment=tvds_segments[segment_index],
                top_horizon_uuid=top_horizon.uuid,
                base_horizon_uuid=base_horizon.uuid,
            )

    return {'in_zone': in_zone_length, 'in_zone_percent': in_zone_length / total_length * 100}


def bulk_calc_zone_statistics(
    project_name: str,
    well_names: str,
    top_horizon: str,
    base_horizon: str,
    landing_point_topset: str,
    landing_point_top: str,
) -> Dict[str, Dict[str, Any]]:
    solo_client = SoloClient(
        client_id=environ.get('ROGII_SOLO_CLIENT_ID'),
        client_secret=environ.get('ROGII_SOLO_CLIENT_SECRET'),
        papi_domain_name=environ.get('ROGII_SOLO_PAPI_DOMAIN_NAME'),
    )
    solo_client.set_project_by_name(project_name)

    statistics = {}

    for well_name in well_names:
        well = solo_client.project.wells.find_by_name(well_name)

        if well is None:
            print(f'Well "{well_name}" not found.')
            continue

        well_data = well.to_dict(get_converted=False)
        calculated_trajectory = calculate_trajectory(
            raw_trajectory=well.trajectory.to_dict(get_converted=False),
            well=well_data,
            measure_units=solo_client.project.measure_unit,
        )

        try:
            statistics[well.name] = calc_zone_statistics(
                well=well,
                calculated_trajectory=calculated_trajectory,
                top_horizon_name=top_horizon,
                base_horizon_name=base_horizon,
                landing_point_topset=landing_point_topset,
                landing_point_top=landing_point_top,
                measure_units=solo_client.project.measure_unit,
            )
        except Exception as exception:
            print(f'Warning! Statistics for well "{well.name}" is not calculated.', exception)

    return statistics


if __name__ == '__main__':
    # Put horizon names for top and base if it's not starred
    script_settings = {
        'project_name': '',
        'well_names': [],
        'top_horizon': '',
        'base_horizon': '',
        'landing_point_topset': '',
        'landing_point_top': '',
    }

    if (not script_settings['landing_point_topset'] and script_settings['landing_point_top']) or (
        script_settings['landing_point_topset'] and not script_settings['landing_point_top']
    ):
        raise Exception('Set correct data for both topset and top, please.')

    zone_statistics = bulk_calc_zone_statistics(**script_settings)

    for well_name in zone_statistics:
        print(f'Well "{well_name}" is {zone_statistics[well_name]}')
