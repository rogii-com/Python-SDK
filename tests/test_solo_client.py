import pytest
from tests.mocks.solo_client import solo_client
from rogii_solo.exceptions import ProjectNotFoundException, InvalidProjectException

project_name = 'Global project'
well_name = 'Lateral'

interpretation_name = 'Interpretation'
starred_interpretation_name = 'Starred Interpretation'

target_line_name = 'Target Line'
starred_target_line_name = 'Starred Target Line'

nested_well_name = 'Nested Well'
starred_nested_well_name = 'Starred Nested Well'


def test_set_project():
    with pytest.raises(ProjectNotFoundException):
        solo_client.set_project_by_name('Non-existent project')

    with pytest.raises(ProjectNotFoundException):
        solo_client.set_project_by_name(None)

    with pytest.raises(InvalidProjectException):
        solo_client.set_project({})

    solo_client.set_project_by_name(project_name)

    assert solo_client.project is not None
    assert solo_client.project.to_dict()['name'] == project_name
    assert solo_client.project.to_df().at[0, 'name'] == project_name


solo_client.set_project_by_name(project_name)
project = solo_client.project


def test_get_projects():
    assert solo_client.projects.to_dict()
    assert not solo_client.projects.to_df().empty


def test_get_project_wells():
    assert project.wells.to_dict()
    assert not project.wells.to_df().empty


def test_get_well():
    well = project.wells.find_by_name(well_name)

    assert well is not None
    assert well.to_dict()['name'] == well_name
    assert well.to_df().at[0, 'name'] == well_name


def test_get_well_trajectory():
    trajectory = project.wells.find_by_name(well_name).trajectory

    assert trajectory.to_dict()
    assert not trajectory.to_df().empty


def test_get_well_trajectory_point():
    trajectory_point = project.wells.find_by_name(well_name).trajectory.find_by_md(0)

    assert trajectory_point is not None
    assert trajectory_point.to_dict()
    assert not trajectory_point.to_df().empty


def test_get_well_interpretations():
    interpretations = project.wells.find_by_name(well_name).interpretations

    assert interpretations.to_dict()
    assert not interpretations.to_df().empty


def test_get_well_interpretation():
    interpretation = project.wells.find_by_name(well_name).interpretations.find_by_name(interpretation_name)

    assert interpretation is not None

    interpretation_data = interpretation.to_dict()

    assert 'meta' in interpretation_data
    assert 'horizons' in interpretation_data
    assert 'segments' in interpretation_data

    assert interpretation_data['meta']['name'] == interpretation_name
    assert interpretation.to_df()['meta'].at[0, 'name'] == interpretation_name


def test_get_well_starred_interpretation():
    starred_interpretation = project.wells.find_by_name(well_name).starred_interpretation

    assert starred_interpretation is not None
    assert starred_interpretation.to_dict()['meta']['name'] == starred_interpretation_name
    assert starred_interpretation.to_df()['meta'].at[0, 'name'] == starred_interpretation_name


def test_get_well_target_lines():
    target_lines = project.wells.find_by_name(well_name).target_lines

    assert target_lines.to_dict()
    assert not target_lines.to_df().empty


def test_get_well_target_line():
    target_line = project.wells.find_by_name(well_name).target_lines.find_by_name(target_line_name)

    assert target_line is not None
    assert target_line.to_dict()['name'] == target_line_name
    assert target_line.to_df().at[0, 'name'] == target_line_name


def test_get_well_starred_target_line():
    starred_target_line = project.wells.find_by_name(well_name).starred_target_line

    assert starred_target_line is not None
    assert starred_target_line.to_dict()['name'] == starred_target_line_name
    assert starred_target_line.to_df().at[0, 'name'] == starred_target_line_name


def test_get_well_nested_wells():
    nested_wells = project.wells.find_by_name(well_name).nested_wells

    assert nested_wells.to_dict()
    assert not nested_wells.to_df().empty


def test_get_well_nested_well():
    nested_well = project.wells.find_by_name(well_name).nested_wells.find_by_name(nested_well_name)

    assert nested_well is not None
    assert nested_well.to_dict()['name'] == nested_well_name
    assert nested_well.to_df().at[0, 'name'] == nested_well_name


def test_get_well_starred_nested_well():
    starred_nested_well = project.wells.find_by_name(well_name).starred_nested_well

    assert starred_nested_well is not None
    assert starred_nested_well.to_dict()['name'] == starred_nested_well_name
    assert starred_nested_well.to_df().at[0, 'name'] == starred_nested_well_name
