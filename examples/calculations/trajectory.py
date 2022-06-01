import copy
from math import acos, cos, fabs, pi, sin, degrees
from typing import Optional

from pandas import DataFrame

from .base import calc_atan2, calc_hypotenuse_length, calc_shape_factor, normalize_angle, calc_vs as base_calc_vs
from .enums import EMeasureUnits
from .constants import DELTA, FEET_TO_METERS


def calculate_trajectory(
        raw_trajectory: DataFrame,
        well: dict,
        measure_unit: EMeasureUnits,
):
    if raw_trajectory.empty or not well:
        return []

    calculated_trajectory = []
    prev_point = None

    for i, raw in raw_trajectory.iterrows():
        point_dict = raw.to_dict()
        calculated_point = calculate_trajectory_point(
            prev_point=prev_point,
            curr_point=prepare_trajectory_point(point_dict, well['convergence']),
            well=well,
            measure_unit=measure_unit,
        )
        calculated_trajectory.append(calculated_point)
        prev_point = calculated_point

    return calculated_trajectory


def calculate_trajectory_point(
        prev_point: dict,
        curr_point: dict,
        well: dict,
        measure_unit: EMeasureUnits,
):
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

    dls = calc_dls(dog_leg, course_length, measure_unit=measure_unit)
    shape = calc_shape(dog_leg, course_length)

    tvd = prev_point['tvd'] + shape * (curr_incl_cos + prev_incl_cos)

    ns = (prev_point['ns'] or 0) + shape * (prev_incl_sin * cos(prev_point['azim']) + curr_incl_sin * cos(curr_azim))
    ew = (prev_point['ew'] or 0) + shape * (prev_incl_sin * sin(prev_point['azim']) + curr_incl_sin * sin(curr_azim))

    calculated_point = dict(
        md=curr_point['md'],
        incl=curr_point['incl'],
        azim=curr_azim,
        tvd=tvd,
        tvt=tvd,
        tvdss=calc_tvdss(well['kb'], tvd),
        ns=ns,
        ew=ew,
        x=calc_x(ew, well['xsrf_real']),
        y=calc_y(ns, well['ysrf_real']),
        vs=calc_vs(ns, ew, well['azimuth']),
        dls=dls,
        dog_leg=dog_leg
    )

    return calculated_point


def interpolate_trajectory_point(
        left_point: dict,
        right_point: dict,
        md: float,
        well: dict,
        measure_unit: EMeasureUnits,
):
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

    x = calc_x(ew, well['xsrf_real'])
    y = calc_y(ns, well['ysrf_real'])
    vs = calc_vs(ns, ew, well['azimuth'])

    incl = calc_atan2(calc_hypotenuse_length(ext_delta_ns, ext_delta_ew), ext_delta_tvd)

    if incl < 0:
        incl += pi

    azim = normalize_angle(calc_atan2(ext_delta_ew, ext_delta_ns))

    dls = calc_dls(dog_leg, course_length, measure_unit=measure_unit)
    point = dict(
        md=md,
        incl=incl,
        azim=azim,
        tvd=tvd,
        tvt=tvd,
        ns=ns,
        ew=ew,
        x=x,
        y=y,
        tvdss=calc_tvdss(kb=well['kb'], tvd=tvd),
        vs=vs,
        dls=dls,
        dog_leg=dog_leg
    )

    return point


def calculate_initial_trajectory_point(
        point: dict,
        well: dict,
):
    tvd = well['tie_in_tvd'] if well['tie_in_tvd'] is not None else point['md']

    point = dict(
        md=point['md'],
        incl=point['incl'],
        azim=normalize_angle(point['azim']),
        tvd=tvd,
        tvt=tvd,
        tvdss=calc_tvdss(well['kb'], tvd),
        ns=well['tie_in_ns'],
        ew=well['tie_in_ew'],
        x=calc_x(well['tie_in_ew'], well['xsrf_real']),
        y=calc_y(well['tie_in_ns'], well['ysrf_real']),
        vs=calc_vs(well['tie_in_ns'], well['tie_in_ew'], well['azimuth']),
        dls=0,
        dog_leg=0
    )
    return point


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


def get_dls_unit_coefficient(measure_unit: EMeasureUnits) -> float:
    return DLS_RADIANS_MAP[measure_unit]


def calc_dls(dog_leg: float, md_delta: float, measure_unit: EMeasureUnits) -> float:
    return degrees(dog_leg) * (get_dls_unit_coefficient(measure_unit) / md_delta)


def calc_shape(dog_leg: float, course_length: float) -> float:
    return 0.5 * calc_shape_factor(dog_leg) * course_length


def prepare_trajectory_point(point: dict, convergence: float):
    prepared_point = copy.deepcopy(point)
    prepared_point['azim'] = prepared_point['azim'] - convergence

    return prepared_point
