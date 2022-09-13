import random
import pytest

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
    STARRED_TOP_TOP_NAME,
    STARRED_TOP_CENTER_NAME,
    STARRED_TOP_BOTTOM_NAME,
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


def test_get_well_trajectory_point(project_papi):
    trajectory_point = project_papi.wells.find_by_name(WELL_NAME).trajectory.find_by_md(0)

    assert trajectory_point is not None

    trajectory_point_data = trajectory_point.to_dict()
    trajectory_point_df = trajectory_point.to_df()

    assert trajectory_point_data
    assert not trajectory_point_df.empty


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


def test_get_nested_well_trajectory_point(project_papi):
    starred_nested_well = project_papi.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    trajectory_point = starred_nested_well.trajectory.find_by_md(0)

    assert trajectory_point is not None

    trajectory_point_data = trajectory_point.to_dict()
    trajectory_point_df = trajectory_point.to_df()

    assert trajectory_point_data
    assert not trajectory_point_df.empty


def test_create_nested_well(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
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


def test_get_project_typewells(project_papi):
    typewells_data = project_papi.typewells.to_dict()
    typewells_df = project_papi.typewells.to_df()

    assert typewells_data
    assert not typewells_df.empty


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


def test_get_typewell_trajectory_point(project_papi):
    trajectory_point = project_papi.typewells.find_by_name(TYPEWELL_NAME).trajectory.find_by_md(0)

    assert trajectory_point is not None

    trajectory_point_data = trajectory_point.to_dict()
    trajectory_point_df = trajectory_point.to_df()

    assert trajectory_point_data
    assert not trajectory_point_df.empty


def test_create_well_topset(project_papi):
    well = project_papi.wells.find_by_name(WELL_NAME)
    topset_name = 'Topset ' + str(random.randint(0, 10000))

    well.create_topset(topset_name)
    assert well.topsets.find_by_name(topset_name) is not None


def test_create_typewell_topset(project_papi):
    typewell = project_papi.typewells.find_by_name(TYPEWELL_NAME)
    topset_name = 'Topset ' + str(random.randint(0, 10000))

    typewell.create_topset(topset_name)
    assert typewell.topsets.find_by_name(topset_name) is not None
    

def test_create_nested_well_topset(project_papi):
    starred_nested_well = project_papi.wells.find_by_name(WELL_NAME).starred_nested_well

    assert starred_nested_well is not None

    topset_name = 'Topset ' + str(random.randint(0, 10000))
    starred_nested_well.create_topset(topset_name)

    assert starred_nested_well.topsets.find_by_name(topset_name) is not None


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
