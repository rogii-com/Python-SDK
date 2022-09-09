import copy
from math import acos, cos, degrees, fabs, pi, sin
from typing import Any, Dict, Optional

from rogii_solo.calculations.base import calc_atan2, calc_hypotenuse_length, calc_shape_factor
from rogii_solo.calculations.base import calc_vs as base_calc_vs
from rogii_solo.calculations.base import normalize_angle
from rogii_solo.calculations.constants import DELTA, FEET_TO_METERS
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.types import RawTrajectory, Trajectory, TrajectoryPoint


def calculate_trajectory(
        raw_trajectory: RawTrajectory,
        well: Dict[str, Any],
        measure_units: EMeasureUnits,
) -> Trajectory:
    if not raw_trajectory or not well:
        return []

    calculated_trajectory = []
    prev_point = None

    for point in raw_trajectory:
        calculated_point = calculate_trajectory_point(
            prev_point=prev_point,
            curr_point=prepare_trajectory_point(point, well['convergence']),
            well=well,
            measure_units=measure_units,
        )
        calculated_trajectory.append(calculated_point)
        prev_point = calculated_point

    return calculated_trajectory


def calculate_trajectory_point(
        prev_point: Dict[str, Any],
        curr_point: Dict[str, Any],
        well: Dict[str, Any],
        measure_units: EMeasureUnits,
) -> TrajectoryPoint:
    if not prev_point:
        return calculate_initial_trajectory_point(curr_point, well)

    course_length = curr_point['md'] - prev_point['md']

    if fabs(course_length) < DELTA:
        return prev_point

    prev_incl_sin, curr_incl_sin = sin(prev_point['incl']), sin(curr_point['incl'])
    prev_incl_cos, curr_incl_cos = cos(prev_point['incl']), cos(curr_point['incl'])

    curr_azim = normalize_angle(curr_point['azim'])

    dog_leg = acos(
        cos(prev_point['incl'] - curr_point['incl'])
        - curr_incl_sin * prev_incl_sin
        * (1.0 - cos(curr_azim - prev_point['azim']))
    )

    dls = calc_dls(dog_leg, course_length, measure_units=measure_units)
    shape = calc_shape(dog_leg, course_length)

    tvd = prev_point['tvd'] + shape * (curr_incl_cos + prev_incl_cos)

    ns = (prev_point['ns'] or 0) + shape * (prev_incl_sin * cos(prev_point['azim']) + curr_incl_sin * cos(curr_azim))
    ew = (prev_point['ew'] or 0) + shape * (prev_incl_sin * sin(prev_point['azim']) + curr_incl_sin * sin(curr_azim))

    return TrajectoryPoint(
        md=curr_point['md'],
        incl=curr_point['incl'],
        azim=curr_azim,
        tvd=tvd,
        tvdss=calc_tvdss(well['kb'], tvd),
        ns=ns,
        ew=ew,
        x=calc_x(ew, well['xsrf']),
        y=calc_y(ns, well['ysrf']),
        vs=calc_vs(ns, ew, well['azimuth']),
        dls=dls,
        dog_leg=dog_leg
    )


def interpolate_trajectory_point(
        left_point: Dict[str, Any],
        right_point: Dict[str, Any],
        md: float,
        well: Dict[str, Any],
        measure_units: EMeasureUnits,
) -> TrajectoryPoint:
    if fabs(md - left_point['md']) < DELTA:
        return left_point

    if fabs(md - right_point['md']) < DELTA:
        return right_point

    point_course_length = right_point['md'] - left_point['md']
    course_length = md - left_point['md']
    dog_leg = (course_length / point_course_length) * right_point['dog_leg']

    shape = calc_shape(dog_leg, course_length)

    left_incl_sin = sin(left_point['incl'])
    left_incl_cos = cos(left_point['incl'])

    left_azim_sin = sin(left_point['azim'])
    left_azim_cos = cos(left_point['azim'])

    dog_leg_sin = sin(dog_leg)
    right_diff_dog_leg_sin = sin(right_point['dog_leg'] - dog_leg)

    right_dog_leg_sin = sin(right_point['dog_leg'])

    left_dog_legged_sin = (
        left_incl_sin / right_dog_leg_sin
        if right_dog_leg_sin < -DELTA or right_dog_leg_sin > DELTA
        else 1.0
    )

    left_dog_legged_cos = (
        left_incl_cos / right_dog_leg_sin
        if right_dog_leg_sin < -DELTA or right_dog_leg_sin > DELTA
        else 1.0
    )

    right_dog_legged_sin = (
        sin(right_point['incl']) / right_dog_leg_sin
        if right_dog_leg_sin < -DELTA or right_dog_leg_sin > DELTA
        else 1.0
    )

    right_dog_legged_cos = (
        cos(right_point['incl']) / right_dog_leg_sin
        if right_dog_leg_sin < -DELTA or right_dog_leg_sin > DELTA
        else 1.0
    )

    ext_delta_tvd = (
        right_diff_dog_leg_sin * left_dog_legged_cos + dog_leg_sin * right_dog_legged_cos
        if right_dog_leg_sin < -DELTA or right_dog_leg_sin > DELTA
        else left_incl_cos
    )

    delta_tvd = shape * (ext_delta_tvd + left_incl_cos)

    ext_delta_ns = (
        right_diff_dog_leg_sin * left_dog_legged_sin * left_azim_cos
        + dog_leg_sin * right_dog_legged_sin * cos(right_point['azim'])
        if right_dog_leg_sin < -DELTA or right_dog_leg_sin > DELTA
        else left_incl_sin * left_azim_cos
    )

    ext_delta_ew = (
        right_diff_dog_leg_sin * left_dog_legged_sin * left_azim_sin
        + dog_leg_sin * right_dog_legged_sin * sin(right_point['azim'])
        if right_point['dog_leg'] < -DELTA or right_point['dog_leg'] > DELTA
        else left_incl_sin * left_azim_sin
    )

    tvd = left_point['tvd'] + delta_tvd

    ns = left_point['ns'] + shape * (ext_delta_ns + left_incl_sin * left_azim_cos)
    ew = left_point['ew'] + shape * (ext_delta_ew + left_incl_sin * left_azim_sin)

    x = calc_x(ew, well['xsrf'])
    y = calc_y(ns, well['ysrf'])
    vs = calc_vs(ns, ew, well['azimuth'])

    incl = calc_atan2(calc_hypotenuse_length(ext_delta_ns, ext_delta_ew), ext_delta_tvd)

    if incl < 0:
        incl += pi

    azim = normalize_angle(calc_atan2(ext_delta_ew, ext_delta_ns))
    dls = calc_dls(dog_leg, course_length, measure_units=measure_units)

    return TrajectoryPoint(
        md=md,
        incl=incl,
        azim=azim,
        tvd=tvd,
        ns=ns,
        ew=ew,
        x=x,
        y=y,
        tvdss=calc_tvdss(kb=well['kb'], tvd=tvd),
        vs=vs,
        dls=dls,
        dog_leg=dog_leg
    )


def calculate_initial_trajectory_point(
        point: Dict[str, Any],
        well: Dict[str, Any],
) -> TrajectoryPoint:
    tvd = well['tie_in_tvd'] if well['tie_in_tvd'] is not None else point['md']

    return TrajectoryPoint(
        md=point['md'],
        incl=point['incl'],
        azim=normalize_angle(point['azim']),
        tvd=tvd,
        tvdss=calc_tvdss(well['kb'], tvd),
        ns=well['tie_in_ns'],
        ew=well['tie_in_ew'],
        x=calc_x(well['tie_in_ew'], well['xsrf']),
        y=calc_y(well['tie_in_ns'], well['ysrf']),
        vs=calc_vs(well['tie_in_ns'], well['tie_in_ew'], well['azimuth']),
        dls=0,
        dog_leg=0
    )


def calc_x(ew: float, xsrf: Optional[float]) -> Optional[float]:
    if xsrf is not None:
        return (ew or 0) + xsrf


def calc_y(ns: float, ysrf: Optional[float]) -> Optional[float]:
    if ysrf is not None:
        return (ns or 0) + ysrf


def calc_vs(ns: float, ew: float, azimuth: float) -> float:
    closure_distance = calc_hypotenuse_length(ns, ew)
    closure_direction = calc_atan2(ew, ns)

    return base_calc_vs(azimuth, closure_distance, closure_direction)


def calc_tvdss(kb: Optional[float], tvd: float) -> Optional[float]:
    if kb is None:
        return

    return kb - tvd


DLS_RADIANS_MAP = {
    EMeasureUnits.METER: 30,
    EMeasureUnits.FOOT: 100 * FEET_TO_METERS,
    EMeasureUnits.METER_FOOT: 100 * FEET_TO_METERS
}


def get_dls_unit_coefficient(measure_units: EMeasureUnits) -> float:
    return DLS_RADIANS_MAP[measure_units]


def calc_dls(dog_leg: float, md_delta: float, measure_units: EMeasureUnits) -> float:
    return degrees(dog_leg) * (get_dls_unit_coefficient(measure_units) / md_delta)


def calc_shape(dog_leg: float, course_length: float) -> float:
    return 0.5 * calc_shape_factor(dog_leg) * course_length


def prepare_trajectory_point(point: Dict[str, Any], convergence: float):
    prepared_point = copy.deepcopy(point)
    prepared_point['azim'] = prepared_point['azim'] - convergence

    return prepared_point
