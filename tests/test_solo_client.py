import pytest
from rogii_solo.exceptions import ProjectNotFoundException, InvalidProjectException

from tests.papi_data import (
    PROJECT_NAME,
    WELL_NAME,
    INTERPRETATION_NAME,
    STARRED_INTERPRETATION_NAME,
    HORIZON_NAME,
    TARGET_LINE_NAME,
    STARRED_TARGET_LINE_NAME,
    NESTED_WELL_NAME,
    STARRED_NESTED_WELL_NAME
)


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

    assert project_data['name'] == PROJECT_NAME
    assert project_df.at[0, 'name'] == PROJECT_NAME


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


def test_get_well_trajectory_point(project):
    trajectory_point = project.wells.find_by_name(WELL_NAME).trajectory.find_by_md(0)

    assert trajectory_point is not None

    trajectory_point_data = trajectory_point.to_dict()
    trajectory_point_df = trajectory_point.to_df()

    assert trajectory_point_data
    assert not trajectory_point_df.empty


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
    assert 'data' in horizon_data

    assert horizon_data['meta']['name'] == HORIZON_NAME
    assert horizon_df['meta'].at[0, 'name'] == HORIZON_NAME

    # TODO: Remove when calculations package is removed
    horizon_data_df = horizon_df['data']

    assert not horizon_data_df.query('md == 0 & tvd.isnull()').empty
    assert not horizon_data_df.query('md == 3858 & tvd.isnull()').empty
    assert not horizon_data_df.query('md == 7452 & tvd.isnull()').empty
    assert not horizon_data_df.query('md == 11257 & tvd.isnull()').empty
    assert not horizon_data_df.query('md == 11288 & tvd == 11517.76902768946').empty
    assert not horizon_data_df.query('md == 13770 & tvd == 11462.009984212762').empty
    assert not horizon_data_df.query('md == 16854 & tvd == 11263.199107699302').empty


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
