from datetime import datetime
from math import fabs
import pytest
import random
from typing import Any

from rogii_solo.calculations.constants import DELTA
from rogii_solo.calculations.converters import radians_to_degrees
from rogii_solo.calculations.interpretation import get_segments, get_segments_with_dip
from rogii_solo.calculations.trajectory import calculate_trajectory
from rogii_solo.exceptions import ProjectNotFoundException, InvalidProjectException
from tests.papi_data import (
    METER_PROJECT_NAME,
    WELL_NAME,
    TYPEWELL_NAME,
    INTERPRETATION_NAME,
    STARRED_INTERPRETATION_NAME,
    STARRED_HORIZON_TOP_NAME,
    STARRED_HORIZON_CENTER_NAME,
    STARRED_HORIZON_BOTTOM_NAME,
    HORIZON_NAME,
    TARGET_LINE_NAME,
    STARRED_TARGET_LINE_NAME,
    NESTED_WELL_NAME,
    STARRED_TOPSET_NAME,
    STARRED_NESTED_WELL_NAME,
    LOG_NAME,
    STARRED_TOP_TOP_NAME,
    STARRED_TOP_CENTER_NAME,
    STARRED_TOP_BOTTOM_NAME,
    MUDLOG_NAME,
    TYPEWELL_XSRF,
    TYPEWELL_YSRF,
    TYPEWELL_KB,
    TRACE_NAME,
    START_DATETIME,
    END_DATETIME,
    EI_LAST_SEGMENT_EXTENDED_NAME
)


def test_auth(solo_client_papi):
    assert solo_client_papi._papi_client.session is not None


def test_get_projects(solo_client_papi):
    projects_data = solo_client_papi.projects.to_dict()
    projects_df = solo_client_papi.projects.to_df()

    assert projects_data
    assert not projects_df.empty


def test_set_non_existent_project(solo_client_papi):
    with pytest.raises(ProjectNotFoundException):
        solo_client_papi.set_project_by_name('Non-existent project')


def test_set_none_project(solo_client_papi):
    with pytest.raises(ProjectNotFoundException):
        solo_client_papi.set_project_by_name(None)


def test_set_invalid_project(solo_client_papi):
    with pytest.raises(InvalidProjectException):
        solo_client_papi.set_project({})


def test_set_project(project_papi):
    assert project_papi is not None

    project_data = project_papi.to_dict()
    project_df = project_papi.to_df()

    assert project_data['name'] == METER_PROJECT_NAME
    assert project_df.at[0, 'name'] == METER_PROJECT_NAME


def test_get_project_wells(project_papi):
    wells_data = project_papi.wells.to_dict()
    wells_df = project_papi.wells.to_df()

    assert wells_data
    assert not wells_df.empty


def test_get_well(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_data = well.to_dict()
    well_df = well.to_df()

    assert well_data['name'] == WELL_NAME
    assert well_df.at[0, 'name'] == WELL_NAME


def test_get_well_trajectory(project_papi):
    trajectory = project_papi.wells.find_by_name(WELL_NAME).trajectory

    trajectory_data = trajectory.to_dict()
    trajectory_df = trajectory.to_df()

    assert trajectory_data
    assert not trajectory_df.empty


def test_get_well_interpretations(project_papi):
    interpretations = project_papi.wells.find_by_name(WELL_NAME).interpretations

    interpretations_data = interpretations.to_dict()
    interpretations_df = interpretations.to_df()

    assert interpretations_data
    assert not interpretations_df.empty


def test_get_well_interpretation(project_papi):
    interpretation = project_papi.wells.find_by_name(WELL_NAME).interpretations.find_by_name(
        INTERPRETATION_NAME
    )

    assert interpretation is not None

    interpretation_data = interpretation.to_dict()
    interpretation_df = interpretation.to_df()

    assert 'meta' in interpretation_data
    assert 'horizons' in interpretation_data
    assert 'segments' in interpretation_data

    assert interpretation_data['meta']['name'] == INTERPRETATION_NAME
    assert interpretation_df['meta'].at[0, 'name'] == INTERPRETATION_NAME


def test_get_well_starred_interpretation(project_papi):
    starred_interpretation = project_papi.wells.find_by_name(WELL_NAME).starred_interpretation

    assert starred_interpretation is not None

    starred_interpretation_data = starred_interpretation.to_dict()
    starred_interpretation_df = starred_interpretation.to_df()

    assert 'meta' in starred_interpretation_data
    assert 'horizons' in starred_interpretation_data
    assert 'segments' in starred_interpretation_data

    assert starred_interpretation_data['meta']['name'] == STARRED_INTERPRETATION_NAME
    assert starred_interpretation_df['meta'].at[0, 'name'] == STARRED_INTERPRETATION_NAME


def test_get_horizon(project_papi):
    starred_interpretation = project_papi.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict()
    horizon_df = horizon.to_df()

    assert 'meta' in horizon_data
    assert 'points' in horizon_data

    assert horizon_data['meta']['name'] == HORIZON_NAME
    assert horizon_df['meta'].at[0, 'name'] == HORIZON_NAME


def test_get_well_target_lines(project_papi):
    target_lines = project_papi.wells.find_by_name(WELL_NAME).target_lines

    target_lines_data = target_lines.to_dict()
    target_lines_df = target_lines.to_df()

    assert target_lines_data
    assert not target_lines_df.empty


def test_get_well_target_line(project_papi):
    target_line = project_papi.wells.find_by_name(WELL_NAME).target_lines.find_by_name(TARGET_LINE_NAME)

    assert target_line is not None

    target_line_data = target_line.to_dict()
    target_line_df = target_line.to_df()

    assert target_line_data['name'] == TARGET_LINE_NAME
    assert target_line_df.at[0, 'name'] == TARGET_LINE_NAME


def test_get_well_starred_target_line(project_papi):
    starred_target_line = project_papi.wells.find_by_name(WELL_NAME).starred_target_line

    assert starred_target_line is not None

    starred_target_line_data = starred_target_line.to_dict()
    starred_target_line_df = starred_target_line.to_df()

    assert starred_target_line_data['name'] == STARRED_TARGET_LINE_NAME
    assert starred_target_line_df.at[0, 'name'] == STARRED_TARGET_LINE_NAME


def test_get_well_nested_wells(project_papi):
    nested_wells = project_papi.wells.find_by_name(WELL_NAME).nested_wells

    nested_wells_data = nested_wells.to_dict()
    nested_wells_df = nested_wells.to_df()

    assert nested_wells_data
    assert not nested_wells_df.empty


def test_get_well_nested_well(project_papi):
    nested_well = project_papi.wells.find_by_name(WELL_NAME).nested_wells.find_by_name(NESTED_WELL_NAME)

    assert nested_well is not None

    nested_well_data = nested_well.to_dict()
    nested_well_df = nested_well.to_df()

    assert nested_well_data['name'] == NESTED_WELL_NAME
    assert nested_well_df.at[0, 'name'] == NESTED_WELL_NAME


def test_get_well_starred_nested_well(project_papi):
    starred_nested_well = project_papi.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_data = starred_nested_well.to_dict()
    starred_nested_well_df = starred_nested_well.to_df()

    assert starred_nested_well_data['name'] == STARRED_NESTED_WELL_NAME
    assert starred_nested_well_df.at[0, 'name'] == STARRED_NESTED_WELL_NAME


def test_get_nested_well_trajectory(project_papi):
    starred_nested_well = project_papi.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory

    trajectory_data = trajectory.to_dict()
    trajectory_df = trajectory.to_df()

    assert trajectory_data
    assert not trajectory_df.empty


def test_create_nested_well(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    nested_well_name = 'Nested Well ' + str(random.randint(0, 10000))
    nested_well_api = f'{nested_well_name} API'
    nested_well_operator = f'{nested_well_name} Operator'

    well.create_nested_well(
        nested_well_name=nested_well_name,
        api=nested_well_api,
        operator=nested_well_operator,
        xsrf=100000.0,
        ysrf=100000.0,
        kb=0.0,
        tie_in_tvd=0.0,
        tie_in_ns=0.0,
        tie_in_ew=0.0
    )
    assert well.nested_wells.find_by_name(nested_well_name) is not None


def test_new_nested_well_header_same_as_parent_well(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    nested_well_name = 'Nested Well ' + str(random.randint(0, 10000))
    nested_well_api = f'{nested_well_name} API'
    nested_well_operator = f'{nested_well_name} Operator'

    well.create_nested_well(
        nested_well_name=nested_well_name,
        api=nested_well_api,
        operator=nested_well_operator,
        xsrf=100000.0,
        ysrf=100000.0,
        kb=0.0,
        tie_in_tvd=0.0,
        tie_in_ns=0.0,
        tie_in_ew=0.0
    )
    new_nested_well = well.nested_wells.find_by_name(nested_well_name)

    assert new_nested_well is not None
    assert new_nested_well.azimuth == well.azimuth
    assert new_nested_well.convergence == well.convergence


def test_get_log(project_papi):
    logs = project_papi.wells.find_by_name(WELL_NAME).logs
    log = logs.find_by_name(LOG_NAME)

    assert log is not None

    log_data = log.to_dict()
    log_df = log.to_df()

    assert 'meta' in log_data
    assert 'points' in log_data

    assert log_data['meta']['name'] == LOG_NAME
    assert log_df['meta'].at[0, 'name'] == LOG_NAME


def test_get_project_typewells(project_papi):
    typewells_data = project_papi.typewells.to_dict()
    typewells_df = project_papi.typewells.to_df()

    assert typewells_data
    assert not typewells_df.empty

    assert typewells_data[0]['name'] == TYPEWELL_NAME
    assert typewells_data[0]['kb'] == TYPEWELL_KB
    assert typewells_data[0]['xsrf'] == TYPEWELL_XSRF
    assert typewells_data[0]['ysrf'] == TYPEWELL_YSRF


def test_get_typewell(project_papi):
    typewell = project_papi.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_data = typewell.to_dict()
    typewell_df = typewell.to_df()

    assert typewell_data['name'] == TYPEWELL_NAME
    assert typewell_df.at[0, 'name'] == TYPEWELL_NAME


def test_get_typewell_trajectory(project_papi):
    trajectory = project_papi.typewells.find_by_name(TYPEWELL_NAME).trajectory

    trajectory_data = trajectory.to_dict()
    trajectory_df = trajectory.to_df()

    assert trajectory_data
    assert not trajectory_df.empty


def test_create_well_topset(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    topset_name = 'Topset ' + str(random.randint(0, 10000))

    assert well.topsets is not None

    well.create_topset(topset_name)
    assert well.topsets.find_by_name(topset_name) is not None


def test_create_typewell_topset(project_papi):
    typewell = project_papi.typewells.find_by_name(TYPEWELL_NAME)
    topset_name = 'Topset ' + str(random.randint(0, 10000))

    assert typewell.topsets is not None

    typewell.create_topset(topset_name)
    assert typewell.topsets.find_by_name(topset_name) is not None


def test_create_nested_well_topset(project_papi):
    starred_nested_well = project_papi.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None
    assert starred_nested_well.topsets is not None

    topset_name = 'Topset ' + str(random.randint(0, 10000))
    starred_nested_well.create_topset(topset_name)

    assert starred_nested_well.topsets.find_by_name(topset_name) is not None


def test_create_well_log(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    log_name = 'Log ' + str(random.randint(0, 10000))

    log_points = [{'index': 0, 'value': 1}]
    well.create_log(log_name=log_name, log_points=log_points)

    assert well.logs.find_by_name(log_name) is not None


def test_create_typewell_log(project_papi):
    typewell = project_papi.typewells.find_by_name(TYPEWELL_NAME)
    log_name = 'Log ' + str(random.randint(0, 10000))

    log_points = [{'index': 0, 'value': 1}]
    typewell.create_log(log_name=log_name, log_points=log_points)

    assert typewell.logs.find_by_name(log_name) is not None


def test_create_target_line(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    target_line_name = 'Target Line ' + str(random.randint(0, 10000))
    well.create_target_line(
        target_line_name=target_line_name,
        origin_x=100.5,
        origin_y=200.5,
        origin_z=300.5,
        target_x=400.5,
        target_y=500.5,
        target_z=600.5
    )

    assert well.target_lines.find_by_name(target_line_name) is not None


def test_create_topset_top(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    topset = well.topsets.find_by_name(STARRED_TOPSET_NAME)

    assert topset is not None

    random_md = random.randint(11400, 11500)
    top_name = 'Top ' + str(random_md)
    topset.create_top(top_name=top_name, md=float(random_md))

    assert topset.tops.find_by_name(top_name) is not None


def test_get_topset_tops(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    topset = well.topsets.find_by_name(STARRED_TOPSET_NAME)

    assert topset is not None

    tops = topset.tops

    assert tops is not None

    tops_data = tops.to_dict()
    tops_df = tops.to_df()

    assert tops_data
    assert not tops_df.empty


def test_get_interpretation_starred_horizons(project_papi):
    starred_interpretation = project_papi.wells.find_by_name(WELL_NAME).starred_interpretation

    assert starred_interpretation is not None
    assert starred_interpretation.starred_horizon_top is not None

    starred_horizon_top_data = starred_interpretation.starred_horizon_top.to_dict()
    starred_horizon_top_df = starred_interpretation.starred_horizon_top.to_df()

    starred_horizon_center_data = starred_interpretation.starred_horizon_center.to_dict()
    starred_horizon_center_df = starred_interpretation.starred_horizon_center.to_df()

    starred_horizon_bottom_data = starred_interpretation.starred_horizon_bottom.to_dict()
    starred_horizon_bottom_df = starred_interpretation.starred_horizon_bottom.to_df()

    assert starred_horizon_top_data['meta']['name'] == STARRED_HORIZON_TOP_NAME
    assert starred_horizon_top_df['meta'].at[0, 'name'] == STARRED_HORIZON_TOP_NAME

    assert starred_horizon_center_data['meta']['name'] == STARRED_HORIZON_CENTER_NAME
    assert starred_horizon_center_df['meta'].at[0, 'name'] == STARRED_HORIZON_CENTER_NAME

    assert starred_horizon_bottom_data['meta']['name'] == STARRED_HORIZON_BOTTOM_NAME
    assert starred_horizon_bottom_df['meta'].at[0, 'name'] == STARRED_HORIZON_BOTTOM_NAME


def test_get_topset_starred_tops(project_papi):
    starred_topset = project_papi.wells.find_by_name(WELL_NAME).starred_topset

    assert starred_topset is not None

    starred_top_top_data = starred_topset.starred_top_top.to_dict()
    starred_top_top_df = starred_topset.starred_top_top.to_df()

    assert starred_top_top_data['name'] == STARRED_TOP_TOP_NAME
    assert starred_top_top_df.at[0, 'name'] == STARRED_TOP_TOP_NAME

    starred_top_center_data = starred_topset.starred_top_center.to_dict()
    starred_top_center_df = starred_topset.starred_top_center.to_df()

    assert starred_top_center_data['name'] == STARRED_TOP_CENTER_NAME
    assert starred_top_center_df.at[0, 'name'] == STARRED_TOP_CENTER_NAME

    starred_top_bottom_data = starred_topset.starred_top_bottom.to_dict()
    starred_top_bottom_df = starred_topset.starred_top_bottom.to_df()

    assert starred_top_bottom_data['name'] == STARRED_TOP_BOTTOM_NAME
    assert starred_top_bottom_df.at[0, 'name'] == STARRED_TOP_BOTTOM_NAME


def test_get_mudlog(project_papi):
    mudlogs = project_papi.wells.find_by_name(WELL_NAME).mudlogs
    mudlog = mudlogs.find_by_name(MUDLOG_NAME)

    assert mudlog is not None

    mudlog_data = mudlog.to_dict()
    mudlog_df = mudlog.to_df()

    assert 'meta' in mudlog_data
    assert 'logs' in mudlog_data

    assert mudlog_data['meta']['name'] == MUDLOG_NAME
    assert mudlog_df.at[0, 'MD'] == mudlog_data['logs'][0]['points'][0]['md']


def test_update_typewell_meta(project_papi):
    typewell = project_papi.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_new_meta = {
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

    typewell.update_meta(**typewell_new_meta)

    assert typewell.name == typewell_new_meta['name']
    assert typewell.operator == typewell_new_meta['operator']
    assert typewell.api == typewell_new_meta['api']
    assert typewell.xsrf == typewell_new_meta['xsrf']
    assert typewell.ysrf == typewell_new_meta['ysrf']
    assert typewell.kb == typewell_new_meta['kb']
    assert typewell.convergence == typewell_new_meta['convergence']
    assert typewell.tie_in_tvd == typewell_new_meta['tie_in_tvd']
    assert typewell.tie_in_ns == typewell_new_meta['tie_in_ns']
    assert typewell.tie_in_ew == typewell_new_meta['tie_in_ew']

    typewell_saved_meta = {
        'name': TYPEWELL_NAME,
        'api': typewell.api,
        'xsrf': TYPEWELL_XSRF,
        'ysrf': TYPEWELL_YSRF,
        'kb': TYPEWELL_KB,
    }
    typewell.update_meta(**typewell_saved_meta)


def test_update_nested_well_meta(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    nested_well = well.nested_wells.find_by_name(NESTED_WELL_NAME)

    assert nested_well is not None

    nested_well_new_meta = {
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

    nested_well.update_meta(**nested_well_new_meta)

    assert nested_well.name == nested_well_new_meta['name']
    assert nested_well.operator == nested_well_new_meta['operator']
    assert nested_well.api == nested_well_new_meta['api']
    assert nested_well.xsrf == nested_well_new_meta['xsrf']
    assert nested_well.ysrf == nested_well_new_meta['ysrf']
    assert nested_well.kb == nested_well_new_meta['kb']
    assert nested_well.tie_in_tvd == nested_well_new_meta['tie_in_tvd']
    assert nested_well.tie_in_ns == nested_well_new_meta['tie_in_ns']
    assert nested_well.tie_in_ew == nested_well_new_meta['tie_in_ew']

    nested_well_saved_meta = {
        'name': NESTED_WELL_NAME,
    }
    nested_well.update_meta(**nested_well_saved_meta)


def test_update_well_meta(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_new_meta = {
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

    well.update_meta(**well_new_meta)

    assert well.name == well_new_meta['name']
    assert well.operator == well_new_meta['operator']
    assert well.api == well_new_meta['api']
    assert well.xsrf == well_new_meta['xsrf']
    assert well.ysrf == well_new_meta['ysrf']
    assert well.kb == well_new_meta['kb']
    assert well.azimuth == well_new_meta['azimuth']
    assert well.convergence == well_new_meta['convergence']
    assert well.tie_in_tvd == well_new_meta['tie_in_tvd']
    assert well.tie_in_ns == well_new_meta['tie_in_ns']
    assert well.tie_in_ew == well_new_meta['tie_in_ew']

    well_saved_meta = {
        'name': WELL_NAME,
    }
    well.update_meta(**well_saved_meta)


def test_get_time_trace(project_papi):
    tz_datetime_template = '%Y-%m-%dT%H:%M:%S.%fZ'
    usual_datetime_template = '%Y-%m-%d %H:%M:%S.%f'

    well = project_papi.wells.find_by_name(WELL_NAME)

    assert well is not None

    time_trace = well.time_traces.find_by_name(TRACE_NAME)

    assert time_trace is not None

    def convert_to_datetime_tz(time_string: str):
        dt = datetime.strptime(time_string, usual_datetime_template)

        return dt.strftime(tz_datetime_template)

    start_datetime_tz = convert_to_datetime_tz(START_DATETIME)
    end_datetime_tz = convert_to_datetime_tz(END_DATETIME)
    time_trace_data = time_trace.to_dict(time_from=start_datetime_tz, time_to=end_datetime_tz)
    time_trace_df = time_trace.to_df(time_from=start_datetime_tz, time_to=end_datetime_tz)

    assert time_trace_data['meta']['name'] == TRACE_NAME

    test_datetime = datetime.strptime(time_trace_data['points'][0]['index'], tz_datetime_template)

    assert test_datetime == datetime.strptime(start_datetime_tz, tz_datetime_template)
    assert time_trace_df['meta'].at[0, 'name'] == TRACE_NAME


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
            measure_units=project_papi.measure_unit
        )
        segments = get_segments(
            well=well_data,
            assembled_segments=interpretation.assembled_segments['segments'],
            calculated_trajectory=calculated_trajectory,
            measure_units=project_papi.measure_unit
        )
        segments_with_dip = get_segments_with_dip(
            segments=segments,
            assembled_horizons=interpretation.assembled_segments['horizons']
        )

        return segments_with_dip[-1]['dip']

    last_segment_dip = get_last_segment_dip(well=well, interpretation=interpretation)
    ei_last_segment_dip = get_last_segment_dip(well=well, interpretation=endless_interpretation)

    assert fabs(last_segment_dip - ei_last_segment_dip) < DELTA


def test_create_well(project_papi):
    # Angles in degrees, depth values in project units
    well_data = {
        'well_name': f'Well_{random.randint(0, 10000)}',
        'operator': f'Operator_{random.randint(0, 10000)}',
        'api': f'Api_{random.randint(0, 10000)}',
        'convergence': random.uniform(0, 10),
        'azimuth': random.uniform(0, 359),
        'kb': random.uniform(0, 100),
        'tie_in_tvd': random.uniform(0, 100),
        'tie_in_ns': random.uniform(0, 100),
        'tie_in_ew': random.uniform(0, 100),
        'xsrf_real': random.uniform(0, 100),
        'ysrf_real': random.uniform(0, 100),
    }

    project_papi.create_well(**well_data)

    well = project_papi.wells.find_by_name(well_data['well_name'])

    assert well is not None

    assert well.operator == well_data['operator']
    assert well.api == well_data['api']
    assert fabs(radians_to_degrees(well.convergence) - well_data['convergence']) < DELTA
    assert fabs(radians_to_degrees(well.azimuth) - well_data['azimuth']) < DELTA
    assert well.kb == well_data['kb']
    assert well.tie_in_tvd == well_data['tie_in_tvd']
    assert well.tie_in_ns == well_data['tie_in_ns']
    assert well.tie_in_ew == well_data['tie_in_ew']
    assert well.xsrf_real == well_data['xsrf_real']
    assert well.ysrf_real == well_data['ysrf_real']


def test_create_typewell(project_papi):
    # Angles in degrees, depth values in project units
    typewell_data = {
        'typewell_name': f'typewell_{random.randint(0, 10000)}',
        'operator': f'Operator_{random.randint(0, 10000)}',
        'api': f'Api_{random.randint(0, 10000)}',
        'convergence': random.uniform(0, 10),
        'kb': random.uniform(0, 100),
        'tie_in_tvd': random.uniform(0, 100),
        'tie_in_ns': random.uniform(0, 100),
        'tie_in_ew': random.uniform(0, 100),
        'xsrf_real': random.uniform(0, 100),
        'ysrf_real': random.uniform(0, 100),
    }

    project_papi.create_typewell(**typewell_data)

    typewell = project_papi.typewells.find_by_name(typewell_data['typewell_name'])

    assert typewell is not None

    assert typewell.operator == typewell_data['operator']
    assert typewell.api == typewell_data['api']
    assert fabs(radians_to_degrees(typewell.convergence) - typewell_data['convergence']) < DELTA
    assert typewell.kb == typewell_data['kb']
    assert typewell.tie_in_tvd == typewell_data['tie_in_tvd']
    assert typewell.tie_in_ns == typewell_data['tie_in_ns']
    assert typewell.tie_in_ew == typewell_data['tie_in_ew']
    assert typewell.xsrf_real == typewell_data['xsrf_real']
    assert typewell.ysrf_real == typewell_data['ysrf_real']


def test_get_well_linked_typewells(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    typewell = project_papi.typewells.find_by_name(TYPEWELL_NAME)

    assert well is not None
    assert typewell is not None

    linked_typewells = well.linked_typewells.to_dict()

    assert linked_typewells[0]['uuid'] == typewell.uuid
