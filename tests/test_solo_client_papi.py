import random
import pytest

from rogii_solo.exceptions import ProjectNotFoundException, InvalidProjectException
from tests.papi_data import (
    PROJECT_NAME,
    WELL_NAME,
    INTERPRETATION_NAME,
    STARRED_INTERPRETATION_NAME,
    TARGET_LINE_NAME,
    STARRED_TARGET_LINE_NAME,
    NESTED_WELL_NAME,
    STARRED_NESTED_WELL_NAME
)


def test_auth(solo_client_papi):
    assert solo_client_papi._papi_client.session is not None


def test_get_projects(solo_client_papi):
    assert solo_client_papi.projects.to_dict()
    assert not solo_client_papi.projects.to_df().empty


def test_set_non_existent_project(solo_client_papi):
    with pytest.raises(ProjectNotFoundException):
        solo_client_papi.set_project_by_name('Non-existent project')


def test_set_none_project(solo_client_papi):
    with pytest.raises(ProjectNotFoundException):
        solo_client_papi.set_project_by_name(None)


def test_set_invalid_project(solo_client_papi):
    with pytest.raises(InvalidProjectException):
        solo_client_papi.set_project({})


def test_set_project(solo_client_papi_project):
    assert solo_client_papi_project is not None
    assert solo_client_papi_project.to_dict()['name'] == PROJECT_NAME
    assert solo_client_papi_project.to_df().at[0, 'name'] == PROJECT_NAME


def test_get_project_wells(solo_client_papi_project):
    assert solo_client_papi_project.wells.to_dict()
    assert not solo_client_papi_project.wells.to_df().empty


def test_get_well(solo_client_papi_project):
    well = solo_client_papi_project.wells.find_by_name(WELL_NAME)

    assert well is not None
    assert well.to_dict()['name'] == WELL_NAME
    assert well.to_df().at[0, 'name'] == WELL_NAME


def test_get_well_trajectory(solo_client_papi_project):
    trajectory = solo_client_papi_project.wells.find_by_name(WELL_NAME).trajectory

    assert trajectory.to_dict()
    assert not trajectory.to_df().empty


def test_get_well_trajectory_point(solo_client_papi_project):
    trajectory_point = solo_client_papi_project.wells.find_by_name(WELL_NAME).trajectory.find_by_md(0)

    assert trajectory_point is not None
    assert trajectory_point.to_dict()
    assert not trajectory_point.to_df().empty


def test_get_well_interpretations(solo_client_papi_project):
    interpretations = solo_client_papi_project.wells.find_by_name(WELL_NAME).interpretations

    assert interpretations.to_dict()
    assert not interpretations.to_df().empty


def test_get_well_interpretation(solo_client_papi_project):
    interpretation = solo_client_papi_project.wells.find_by_name(WELL_NAME).interpretations.find_by_name(
        INTERPRETATION_NAME
    )

    assert interpretation is not None

    interpretation_data = interpretation.to_dict()

    assert 'meta' in interpretation_data
    assert 'horizons' in interpretation_data
    assert 'segments' in interpretation_data

    assert interpretation_data['meta']['name'] == INTERPRETATION_NAME
    assert interpretation.to_df()['meta'].at[0, 'name'] == INTERPRETATION_NAME


def test_get_well_starred_interpretation(solo_client_papi_project):
    starred_interpretation = solo_client_papi_project.wells.find_by_name(WELL_NAME).starred_interpretation

    assert starred_interpretation is not None
    assert starred_interpretation.to_dict()['meta']['name'] == STARRED_INTERPRETATION_NAME
    assert starred_interpretation.to_df()['meta'].at[0, 'name'] == STARRED_INTERPRETATION_NAME


def test_get_well_target_lines(solo_client_papi_project):
    target_lines = solo_client_papi_project.wells.find_by_name(WELL_NAME).target_lines

    assert target_lines.to_dict()
    assert not target_lines.to_df().empty


def test_get_well_target_line(solo_client_papi_project):
    target_line = solo_client_papi_project.wells.find_by_name(WELL_NAME).target_lines.find_by_name(TARGET_LINE_NAME)

    assert target_line is not None
    assert target_line.to_dict()['name'] == TARGET_LINE_NAME
    assert target_line.to_df().at[0, 'name'] == TARGET_LINE_NAME


def test_get_well_starred_target_line(solo_client_papi_project):
    starred_target_line = solo_client_papi_project.wells.find_by_name(WELL_NAME).starred_target_line

    assert starred_target_line is not None
    assert starred_target_line.to_dict()['name'] == STARRED_TARGET_LINE_NAME
    assert starred_target_line.to_df().at[0, 'name'] == STARRED_TARGET_LINE_NAME


def test_get_well_nested_wells(solo_client_papi_project):
    nested_wells = solo_client_papi_project.wells.find_by_name(WELL_NAME).nested_wells

    assert nested_wells.to_dict()
    assert not nested_wells.to_df().empty


def test_get_well_nested_well(solo_client_papi_project):
    nested_well = solo_client_papi_project.wells.find_by_name(WELL_NAME).nested_wells.find_by_name(NESTED_WELL_NAME)

    assert nested_well is not None
    assert nested_well.to_dict()['name'] == NESTED_WELL_NAME
    assert nested_well.to_df().at[0, 'name'] == NESTED_WELL_NAME


def test_get_well_starred_nested_well(solo_client_papi_project):
    starred_nested_well = solo_client_papi_project.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None
    assert starred_nested_well.to_dict()['name'] == STARRED_NESTED_WELL_NAME
    assert starred_nested_well.to_df().at[0, 'name'] == STARRED_NESTED_WELL_NAME


def test_create_nested_well(solo_client_papi_project):
    well = solo_client_papi_project.wells.find_by_name(WELL_NAME)
    nested_well_name = 'Nested Well ' + str(random.randint(0, 10000))

    well.create_nested_well(
        nested_well_name=nested_well_name,
        operator='Operator',
        api=nested_well_name,
        xsrf=100000.0,
        ysrf=100000.0,
        kb=0.0,
        tie_in_tvd=0.0,
        tie_in_ns=0.0,
        tie_in_ew=0.0
    )
    assert well.nested_wells.find_by_name(nested_well_name) is not None
