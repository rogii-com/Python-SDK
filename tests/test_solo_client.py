from datetime import datetime
from math import fabs

import pytest

from rogii_solo.calculations.interpretation import get_last_segment_dip
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
    EI_LAST_SEGMENT_EXTENDED_ID,
    EI_LAST_SEGMENT_OUT_ID,
    EI_ALL_SEGMENTS_OUT_ID
)

DELTA_EI_DIP = 0.001


def test_get_projects(solo_client):
    projects_data = solo_client.projects.to_dict()
    projects_df = solo_client.projects.to_df()

    assert projects_data
    assert not projects_df.empty


def test_set_non_existent_project(solo_client):
    with pytest.raises(ProjectNotFoundException):
        solo_client.set_project_by_name('Non-existent project')


def test_set_none_project(solo_client):
    with pytest.raises(ProjectNotFoundException):
        solo_client.set_project_by_name(None)


def test_set_invalid_project(solo_client):
    with pytest.raises(InvalidProjectException):
        solo_client.set_project({})


def test_set_project(project):
    assert project is not None

    project_data = project.to_dict()
    project_df = project.to_df()

    assert project_data['name'] == METER_PROJECT_NAME
    assert project_df.at[0, 'name'] == METER_PROJECT_NAME


def test_get_project_wells(project):
    wells_data = project.wells.to_dict()
    wells_df = project.wells.to_df()

    assert wells_data
    assert not wells_df.empty


def test_get_well(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    well_data = well.to_dict()
    well_df = well.to_df()

    assert well_data['name'] == WELL_NAME
    assert well_df.at[0, 'name'] == WELL_NAME


def test_get_well_trajectory(project):
    trajectory = project.wells.find_by_name(WELL_NAME).trajectory

    trajectory_data = trajectory.to_dict()
    trajectory_df = trajectory.to_df()

    assert trajectory_data
    assert not trajectory_df.empty


def test_get_well_interpretations(project):
    interpretations = project.wells.find_by_name(WELL_NAME).interpretations

    interpretations_data = interpretations.to_dict()
    interpretations_df = interpretations.to_df()

    assert interpretations_data
    assert not interpretations_df.empty


def test_get_well_interpretation(project):
    interpretation = project.wells.find_by_name(WELL_NAME).interpretations.find_by_name(
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


def test_get_well_starred_interpretation(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation

    assert starred_interpretation is not None

    starred_interpretation_data = starred_interpretation.to_dict()
    starred_interpretation_df = starred_interpretation.to_df()

    assert 'meta' in starred_interpretation_data
    assert 'horizons' in starred_interpretation_data
    assert 'segments' in starred_interpretation_data

    assert starred_interpretation_data['meta']['name'] == STARRED_INTERPRETATION_NAME
    assert starred_interpretation_df['meta'].at[0, 'name'] == STARRED_INTERPRETATION_NAME


def test_get_horizon(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation
    horizon = starred_interpretation.horizons.find_by_name(HORIZON_NAME)

    assert horizon is not None

    horizon_data = horizon.to_dict()
    horizon_df = horizon.to_df()

    assert 'meta' in horizon_data
    assert 'points' in horizon_data

    assert horizon_data['meta']['name'] == HORIZON_NAME
    assert horizon_df['meta'].at[0, 'name'] == HORIZON_NAME


def test_get_well_target_lines(project):
    target_lines = project.wells.find_by_name(WELL_NAME).target_lines

    target_lines_data = target_lines.to_dict()
    target_lines_df = target_lines.to_df()

    assert target_lines_data
    assert not target_lines_df.empty


def test_get_well_target_line(project):
    target_line = project.wells.find_by_name(WELL_NAME).target_lines.find_by_name(TARGET_LINE_NAME)

    assert target_line is not None

    target_line_data = target_line.to_dict()
    target_line_df = target_line.to_df()

    assert target_line_data['name'] == TARGET_LINE_NAME
    assert target_line_df.at[0, 'name'] == TARGET_LINE_NAME


def test_get_well_starred_target_line(project):
    starred_target_line = project.wells.find_by_name(WELL_NAME).starred_target_line

    assert starred_target_line is not None

    starred_target_line_data = starred_target_line.to_dict()
    starred_target_line_df = starred_target_line.to_df()

    assert starred_target_line_data['name'] == STARRED_TARGET_LINE_NAME
    assert starred_target_line_df.at[0, 'name'] == STARRED_TARGET_LINE_NAME


def test_get_well_nested_wells(project):
    nested_wells = project.wells.find_by_name(WELL_NAME).nested_wells

    nested_wells_data = nested_wells.to_dict()
    nested_wells_df = nested_wells.to_df()

    assert nested_wells_data
    assert not nested_wells_df.empty


def test_get_well_nested_well(project):
    nested_well = project.wells.find_by_name(WELL_NAME).nested_wells.find_by_name(NESTED_WELL_NAME)

    assert nested_well is not None

    nested_well_data = nested_well.to_dict()
    nested_well_df = nested_well.to_df()

    assert nested_well_data['name'] == NESTED_WELL_NAME
    assert nested_well_df.at[0, 'name'] == NESTED_WELL_NAME


def test_get_well_starred_nested_well(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    starred_nested_well_data = starred_nested_well.to_dict()
    starred_nested_well_df = starred_nested_well.to_df()

    assert starred_nested_well_data['name'] == STARRED_NESTED_WELL_NAME
    assert starred_nested_well_df.at[0, 'name'] == STARRED_NESTED_WELL_NAME


def test_get_nested_well_trajectory(project):
    starred_nested_well = project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory = starred_nested_well.trajectory

    trajectory_data = trajectory.to_dict()
    trajectory_df = trajectory.to_df()

    assert trajectory_data
    assert not trajectory_df.empty


def test_get_log(project):
    logs = project.wells.find_by_name(WELL_NAME).logs
    log = logs.find_by_name(LOG_NAME)

    assert log is not None

    log_data = log.to_dict()
    log_df = log.to_df()

    assert 'meta' in log_data
    assert 'points' in log_data

    assert log_data['meta']['name'] == LOG_NAME
    assert log_df['meta'].at[0, 'name'] == LOG_NAME


def test_get_project_typewells(project):
    typewells_data = project.typewells.to_dict()
    typewells_df = project.typewells.to_df()

    assert typewells_data
    assert not typewells_df.empty

    assert typewells_data[0]['name'] == TYPEWELL_NAME
    assert typewells_data[0]['kb'] == TYPEWELL_KB
    assert typewells_data[0]['xsrf'] == TYPEWELL_XSRF
    assert typewells_data[0]['ysrf'] == TYPEWELL_YSRF


def test_get_typewell(project):
    typewell = project.typewells.find_by_name(TYPEWELL_NAME)

    assert typewell is not None

    typewell_data = typewell.to_dict()
    typewell_df = typewell.to_df()

    assert typewell_data['name'] == TYPEWELL_NAME
    assert typewell_df.at[0, 'name'] == TYPEWELL_NAME


def test_get_typewell_trajectory(project):
    trajectory = project.typewells.find_by_name(TYPEWELL_NAME).trajectory

    trajectory_data = trajectory.to_dict()
    trajectory_df = trajectory.to_df()

    assert trajectory_data
    assert not trajectory_df.empty


def test_get_topset_tops(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    topset = well.topsets.find_by_name(STARRED_TOPSET_NAME)

    assert topset is not None

    tops = topset.tops

    assert tops is not None

    tops_data = tops.to_dict()
    tops_df = tops.to_df()

    assert tops_data
    assert not tops_df.empty


def test_get_interpretation_starred_horizons(project):
    starred_interpretation = project.wells.find_by_name(WELL_NAME).starred_interpretation

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


def test_get_topset_starred_tops(project):
    starred_topset = project.wells.find_by_name(WELL_NAME).starred_topset

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


def test_get_mudlog(project):
    mudlogs = project.wells.find_by_name(WELL_NAME).mudlogs
    mudlog = mudlogs.find_by_name(MUDLOG_NAME)

    assert mudlog is not None

    mudlog_data = mudlog.to_dict()
    mudlog_df = mudlog.to_df()

    assert 'meta' in mudlog_data
    assert 'logs' in mudlog_data

    assert mudlog_data['meta']['name'] == MUDLOG_NAME
    assert mudlog_df.at[0, 'MD'] == mudlog_data['logs'][0]['points'][0]['md']


def test_get_time_trace(project):
    tz_datetime_template = '%Y-%m-%dT%H:%M:%S.%fZ'
    usual_datetime_template = '%Y-%m-%d %H:%M:%S.%f'

    well = project.wells.find_by_name(WELL_NAME)

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


def test_get_well_linked_typewells(project):
    well = project.wells.find_by_name(WELL_NAME)
    typewell = project.typewells.find_by_name(TYPEWELL_NAME)

    assert well is not None
    assert typewell is not None

    linked_typewells = well.linked_typewells.to_dict()

    assert linked_typewells[0]['uuid'] == typewell.uuid


def test_ei_last_segment_extended(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    interpretation = well.starred_interpretation
    endless_interpretation = well.interpretations.find_by_id(EI_LAST_SEGMENT_EXTENDED_ID)

    assert interpretation is not None
    assert endless_interpretation is not None

    _test_ei_case(
        well=well,
        interpretation=interpretation,
        endless_interpretation=endless_interpretation,
        measure_units=project.measure_unit
    )


def test_ei_last_segment_out(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    interpretation = well.starred_interpretation
    endless_interpretation = well.interpretations.find_by_id(EI_LAST_SEGMENT_OUT_ID)

    assert interpretation is not None
    assert endless_interpretation is not None

    _test_ei_case(
        well=well,
        interpretation=interpretation,
        endless_interpretation=endless_interpretation,
        measure_units=project.measure_unit
    )


def test_ei_all_segments_out(project):
    well = project.wells.find_by_name(WELL_NAME)

    assert well is not None

    interpretation = well.starred_interpretation
    endless_interpretation = well.interpretations.find_by_id(EI_ALL_SEGMENTS_OUT_ID)

    assert interpretation is not None
    assert endless_interpretation is not None

    endless_interpretation_data = endless_interpretation.to_dict()

    assert endless_interpretation_data['horizons'] is None
    assert endless_interpretation_data['segments'] is None


def _test_ei_case(well, interpretation, endless_interpretation, measure_units):
    interpretation_data = interpretation.to_dict()
    endless_interpretation_data = endless_interpretation.to_dict()

    last_segment = interpretation_data['segments'][-1]
    ei_last_segment = endless_interpretation_data['segments'][-1]

    assert last_segment['md'] == ei_last_segment['md']

    last_segment_dip = get_last_segment_dip(
        well=well,
        assembled_segments=interpretation.assembled_segments,
        measure_units=measure_units
    )
    ei_last_segment_dip = get_last_segment_dip(
        well=well,
        assembled_segments=endless_interpretation.assembled_segments,
        measure_units=measure_units
    )

    assert fabs(last_segment_dip - ei_last_segment_dip) < DELTA_EI_DIP
