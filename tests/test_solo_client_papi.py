import random
import pytest

from rogii_solo.exceptions import ProjectNotFoundException, InvalidProjectException
from tests.papi_data import (
    METER_PROJECT_NAME,
    WELL_NAME,
    INTERPRETATION_NAME,
    STARRED_INTERPRETATION_NAME,
    HORIZON_NAME,
    TARGET_LINE_NAME,
    STARRED_TARGET_LINE_NAME,
    NESTED_WELL_NAME,
    STARRED_NESTED_WELL_NAME,
    LOG_NAME
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
