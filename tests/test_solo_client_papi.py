import random
from math import fabs
from typing import Any

from rogii_solo.calculations.constants import DELTA
from rogii_solo.calculations.interpretation import get_segments, get_segments_with_dip
from rogii_solo.calculations.trajectory import calculate_trajectory
from tests.papi_data import (
    EI_LAST_SEGMENT_EXTENDED_NAME,
    NESTED_WELL_NAME,
    STARRED_NESTED_WELL_NAME,
    STARRED_TOPSET_NAME,
    TYPEWELL_NAME,
    WELL_NAME,
)
from tests.utils import np_is_close


def test_auth(solo_client_papi):
    assert solo_client_papi._papi_client.session is not None


def test_get_projects(solo_client_papi):
    projects_data = solo_client_papi.projects.to_dict()
    projects_df = solo_client_papi.projects.to_df()

    assert projects_data
    assert not projects_df.empty


def test_create_project_well(project_papi):
    # Angles in degrees, depth values in project units
    wells = project_papi.wells
    input_data = {
        'name': f'Well {random.randint(0, 10000)}',
        'api': f'Well API {random.randint(0, 10000)}',
        'operator': f'Well Operator {random.randint(0, 10000)}',
        'convergence': random.uniform(0, 10),
        'azimuth': random.uniform(0, 359),
        'kb': random.uniform(0, 100),
        'tie_in_tvd': random.uniform(0, 100),
        'tie_in_ns': random.uniform(0, 100),
        'tie_in_ew': random.uniform(0, 100),
        'xsrf_real': random.uniform(0, 100),
        'ysrf_real': random.uniform(0, 100),
    }
    project_papi.create_well(**input_data)

    well = wells.find_by_name(input_data['name'])
    assert well is not None

    well_data = well.to_dict()

    assert well_data['name'] == input_data['name']
    assert well_data['operator'] == input_data['operator']
    assert well_data['api'] == input_data['api']
    assert np_is_close(well_data['convergence'], input_data['convergence'])
    assert np_is_close(well_data['azimuth'], input_data['azimuth'])
    assert np_is_close(well_data['kb'], input_data['kb'])
    assert np_is_close(well_data['tie_in_tvd'], input_data['tie_in_tvd'])
    assert np_is_close(well_data['tie_in_ns'], input_data['tie_in_ns'])
    assert np_is_close(well_data['tie_in_ew'], input_data['tie_in_ew'])
    assert np_is_close(well_data['xsrf_real'], input_data['xsrf_real'])
    assert np_is_close(well_data['ysrf_real'], input_data['ysrf_real'])


def test_create_project_typewell(project_papi):
    # Angles in degrees, depth values in project units
    typewells = project_papi.typewells
    input_data = {
        'name': f'Typewell {random.randint(0, 10000)}',
        'api': 'Typewell API',
        'operator': 'Typewell Operator',
        'convergence': random.uniform(0, 10),
        'kb': random.uniform(0, 100),
        'tie_in_tvd': random.uniform(0, 100),
        'tie_in_ns': random.uniform(0, 100),
        'tie_in_ew': random.uniform(0, 100),
        'xsrf_real': random.uniform(0, 100),
        'ysrf_real': random.uniform(0, 100),
    }
    project_papi.create_typewell(**input_data)

    typewell = typewells.find_by_name(input_data['name'])
    assert typewell is not None

    typewell_data = typewell.to_dict()

    assert typewell_data['name'] == input_data['name']
    assert typewell_data['operator'] == input_data['operator']
    assert typewell_data['api'] == input_data['api']
    assert np_is_close(typewell_data['convergence'], input_data['convergence'])
    assert np_is_close(typewell_data['kb'], input_data['kb'])
    assert np_is_close(typewell_data['tie_in_tvd'], input_data['tie_in_tvd'])
    assert np_is_close(typewell_data['tie_in_ns'], input_data['tie_in_ns'])
    assert np_is_close(typewell_data['tie_in_ew'], input_data['tie_in_ew'])
    assert np_is_close(typewell_data['xsrf_real'], input_data['xsrf_real'])
    assert np_is_close(typewell_data['ysrf_real'], input_data['ysrf_real'])


def test_create_well_nested_well(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    assert well is not None

    nested_wells = well.nested_wells
    input_data = {
        'name': f'Nested Well {random.randint(0, 10000)}',
        'api': 'Nested Well API',
        'operator': 'Nested Well Operator',
        'xsrf': random.uniform(0, 100),
        'ysrf': random.uniform(0, 100),
        'kb': random.uniform(0, 100),
        'tie_in_tvd': random.uniform(0, 100),
        'tie_in_ns': random.uniform(0, 100),
        'tie_in_ew': random.uniform(0, 100),
    }
    well.create_nested_well(**input_data)

    nested_well = nested_wells.find_by_name(input_data['name'])
    assert nested_well is not None

    well_data = well.to_dict()
    nested_well_data = nested_well.to_dict()

    assert nested_well_data['name'] == input_data['name']
    assert nested_well_data['api'] == input_data['api']
    assert nested_well_data['operator'] == input_data['operator']

    assert np_is_close(nested_well_data['azimuth'], well_data['azimuth'])
    assert np_is_close(nested_well_data['convergence'], well_data['convergence'])

    assert np_is_close(nested_well_data['xsrf'], input_data['xsrf'])
    assert np_is_close(nested_well_data['ysrf'], input_data['ysrf'])
    assert np_is_close(nested_well_data['kb'], input_data['kb'])
    assert np_is_close(nested_well_data['tie_in_tvd'], input_data['tie_in_tvd'])
    assert np_is_close(nested_well_data['tie_in_ns'], input_data['tie_in_ns'])
    assert np_is_close(nested_well_data['tie_in_ew'], input_data['tie_in_ew'])


def test_create_well_target_line(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    assert well is not None

    target_lines = well.target_lines
    input_data = {
        'name': f'Target Line {random.randint(0, 10000)}',
        'origin_x': 100.5,
        'origin_y': 200.5,
        'origin_z': 300.5,
        'target_x': 400.5,
        'target_y': 500.5,
        'target_z': 600.5,
    }
    well.create_target_line(**input_data)
    target_line = target_lines.find_by_name(input_data['name'])
    assert target_line is not None

    target_line_data = target_line.to_dict()

    assert np_is_close(target_line_data['origin_x'], input_data['origin_x'])
    assert np_is_close(target_line_data['origin_y'], input_data['origin_y'])
    assert np_is_close(target_line_data['origin_z'], input_data['origin_z'])
    assert np_is_close(target_line_data['target_x'], input_data['target_x'])
    assert np_is_close(target_line_data['target_y'], input_data['target_y'])
    assert np_is_close(target_line_data['target_z'], input_data['target_z'])


def test_create_well_topset(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    assert well is not None

    topsets = well.topsets
    topset_name = f'Topset {random.randint(0, 10000)}'

    well.create_topset(topset_name)
    topset = topsets.find_by_name(topset_name)
    assert topset is not None

    topset_data = topset.to_dict()
    assert topset_data['name'] == topset_name


def test_create_typewell_topset(project_papi):
    typewell = project_papi.typewells.find_by_name(TYPEWELL_NAME)
    assert typewell is not None

    topsets = typewell.topsets
    topset_name = f'Topset {random.randint(0, 10000)}'

    typewell.create_topset(topset_name)
    topset = topsets.find_by_name(topset_name)
    assert topset is not None

    topset_data = topset.to_dict()
    assert topset_data['name'] == topset_name


def test_create_nested_well_topset(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    assert well is not None

    nested_well = well.nested_wells.find_by_name(STARRED_NESTED_WELL_NAME)
    assert nested_well is not None

    topsets = nested_well.topsets
    topset_name = f'Topset {random.randint(0, 10000)}'

    nested_well.create_topset(topset_name)
    topset = topsets.find_by_name(topset_name)
    assert topset is not None

    topset_data = topset.to_dict()
    assert topset_data['name'] == topset_name


def test_create_well_log(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    assert well is not None

    logs = well.logs
    log_name = 'Log ' + str(random.randint(0, 10000))
    log_points = [{'index': 0, 'value': 1}]

    well.create_log(name=log_name, points=log_points)
    assert logs.find_by_name(log_name) is not None


def test_create_typewell_log(project_papi):
    typewell = project_papi.typewells.find_by_name(TYPEWELL_NAME)
    assert typewell is not None

    logs = typewell.logs
    log_name = f'Log {random.randint(0, 10000)}'
    log_points = [{'index': 0, 'value': 1}]

    typewell.create_log(name=log_name, points=log_points)
    assert logs.find_by_name(log_name) is not None


def test_create_topset_top(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    assert well is not None

    topset = well.topsets.find_by_name(STARRED_TOPSET_NAME)
    assert topset is not None

    tops = topset.tops
    input_data = {
        'name': f'Top {random.randint(0, 10000)}',
        'md': random.randint(11400, 11500),
    }
    topset.create_top(**input_data)

    top = tops.find_by_name(input_data['name'])
    assert top is not None

    top_data = top.to_dict()

    assert top_data['name'] == input_data['name']
    assert np_is_close(top_data['md'], input_data['md'])


def test_update_well_meta(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    assert well is not None

    input_data = {
        'name': f'Well {random.randint(0, 1000)}',
        'operator': f'Operator {random.randint(0, 1000)}',
        'api': f'API {random.randint(0, 1000)}',
        'xsrf': random.randint(0, 100),
        'ysrf': random.randint(0, 100),
        'kb': random.randint(0, 100),
        'azimuth': random.randint(0, 270),
        'convergence': random.randint(0, 10),
        'tie_in_tvd': random.randint(0, 100),
        'tie_in_ns': random.randint(0, 100),
        'tie_in_ew': random.randint(0, 100),
    }
    well.update_meta(**input_data)

    well_data = well.to_dict()

    assert well_data['name'] == input_data['name']
    assert well_data['api'] == input_data['api']
    assert well_data['operator'] == input_data['operator']
    assert np_is_close(well_data['xsrf'], input_data['xsrf'])
    assert np_is_close(well_data['ysrf'], input_data['ysrf'])
    assert np_is_close(well_data['kb'], input_data['kb'])
    assert np_is_close(well_data['azimuth'], input_data['azimuth'])
    assert np_is_close(well_data['convergence'], input_data['convergence'])
    assert np_is_close(well_data['tie_in_tvd'], input_data['tie_in_tvd'])
    assert np_is_close(well_data['tie_in_ns'], input_data['tie_in_ns'])
    assert np_is_close(well_data['tie_in_ew'], input_data['tie_in_ew'])


def test_update_typewell_meta(project_papi):
    typewell = project_papi.typewells.find_by_name(TYPEWELL_NAME)
    assert typewell is not None

    input_data = {
        'name': f'Typewell {random.randint(0, 1000)}',
        'operator': f'Operator {random.randint(0, 1000)}',
        'api': f'API {random.randint(0, 1000)}',
        'xsrf': random.randint(0, 100),
        'ysrf': random.randint(0, 100),
        'kb': random.randint(0, 100),
        'convergence': random.randint(0, 10),
        'tie_in_tvd': random.randint(0, 100),
        'tie_in_ns': random.randint(0, 100),
        'tie_in_ew': random.randint(0, 100),
    }
    typewell.update_meta(**input_data)

    typewell_data = typewell.to_dict()

    assert typewell_data['name'] == input_data['name']
    assert typewell_data['api'] == input_data['api']
    assert typewell_data['operator'] == input_data['operator']
    assert np_is_close(typewell_data['xsrf'], input_data['xsrf'])
    assert np_is_close(typewell_data['ysrf'], input_data['ysrf'])
    assert np_is_close(typewell_data['kb'], input_data['kb'])
    assert np_is_close(typewell_data['convergence'], input_data['convergence'])
    assert np_is_close(typewell_data['tie_in_tvd'], input_data['tie_in_tvd'])
    assert np_is_close(typewell_data['tie_in_ns'], input_data['tie_in_ns'])
    assert np_is_close(typewell_data['tie_in_ew'], input_data['tie_in_ew'])


def test_update_nested_well_meta(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    assert well is not None

    nested_well = well.nested_wells.find_by_name(NESTED_WELL_NAME)
    assert nested_well is not None

    input_data = {
        'name': f'Nested Well {random.randint(0, 1000)}',
        'operator': f'Operator {random.randint(0, 1000)}',
        'api': f'API {random.randint(0, 1000)}',
        'xsrf': random.randint(0, 100),
        'ysrf': random.randint(0, 100),
        'kb': random.randint(0, 100),
        'tie_in_tvd': random.randint(0, 100),
        'tie_in_ns': random.randint(0, 100),
        'tie_in_ew': random.randint(0, 100),
    }
    nested_well.update_meta(**input_data)

    nested_well_data = nested_well.to_dict()

    assert nested_well_data['name'] == input_data['name']
    assert nested_well_data['api'] == input_data['api']
    assert nested_well_data['operator'] == input_data['operator']
    assert np_is_close(nested_well_data['xsrf'], input_data['xsrf'])
    assert np_is_close(nested_well_data['ysrf'], input_data['ysrf'])
    assert np_is_close(nested_well_data['kb'], input_data['kb'])
    assert np_is_close(nested_well_data['tie_in_tvd'], input_data['tie_in_tvd'])
    assert np_is_close(nested_well_data['tie_in_ns'], input_data['tie_in_ns'])
    assert np_is_close(nested_well_data['tie_in_ew'], input_data['tie_in_ew'])


def test_endless_interpretation_dips(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    interpretation = well.starred_interpretation
    endless_interpretation = well.interpretations.find_by_name(EI_LAST_SEGMENT_EXTENDED_NAME)

    assert interpretation is not None
    assert endless_interpretation is not None

    interpretation_data = interpretation.to_dict()
    endless_interpretation_data = endless_interpretation.to_dict()

    last_segment = interpretation_data['segments'][-1]
    ei_last_segment = endless_interpretation_data['segments'][-1]

    assert last_segment['md'] == ei_last_segment['md']

    def get_last_segment_dip(well: Any, interpretation: Any):
        well_data = well.to_dict(get_converted=False)
        calculated_trajectory = calculate_trajectory(
            raw_trajectory=well.trajectory.to_dict(get_converted=False),
            well=well_data,
            measure_units=project_papi.measure_unit,
        )
        segments = get_segments(
            well=well_data,
            assembled_segments=interpretation.assembled_segments['segments'],
            calculated_trajectory=calculated_trajectory,
            measure_units=project_papi.measure_unit,
        )
        segments_with_dip = get_segments_with_dip(
            segments=segments, assembled_horizons=interpretation.assembled_segments['horizons']
        )

        return segments_with_dip[-1]['dip']

    last_segment_dip = get_last_segment_dip(well=well, interpretation=interpretation)
    ei_last_segment_dip = get_last_segment_dip(well=well, interpretation=endless_interpretation)

    assert fabs(last_segment_dip - ei_last_segment_dip) < DELTA


def test_get_time_trace(project_papi):
    start_datetime = '2020-09-13T10:53:17Z'

    well = project_papi.wells.find_by_name('wellbore timelog')
    assert well is not None

    time_traces = well.time_traces
    assert time_traces is not None

    time_trace = time_traces.find_by_name('Bit depth')
    assert time_trace is not None

    trace_points = time_trace.points
    assert trace_points is not None

    trace_points_data = trace_points.to_dict()
    assert trace_points_data
    assert len(trace_points_data) == len(trace_points)

    trace_points_data = trace_points.to_dict(time_from=start_datetime)
    assert trace_points_data
    assert len(trace_points_data) == 3


def test_get_calc_trace(project_papi):
    start_datetime = '2020-09-13T10:53:01Z'

    well = project_papi.wells.find_by_name('wellbore timelog')
    assert well is not None

    calc_traces = well.calc_traces
    assert calc_traces is not None

    calc_trace = calc_traces.find_by_name('Rig Activity')
    assert calc_trace is not None

    trace_points = calc_trace.points
    assert trace_points is not None

    trace_points_data = trace_points.to_dict()
    assert trace_points_data
    assert len(trace_points_data) == len(trace_points)

    trace_points_data = trace_points.to_dict(time_from=start_datetime)
    assert trace_points_data
    assert len(trace_points_data) == 3
