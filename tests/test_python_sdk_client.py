import random
from os import environ

from python_sdk.client import SoloClient

project_name = 'Global project'
well_name = 'Lateral'
interpretation_name = 'Interpretation'
starred_interpretation_name = 'Interpretation'
target_line_name = 'Target Line'
nested_well_name = 'Nested Well'

client = SoloClient(
    client_id=environ.get('CLIENT_ID'),
    client_secret=environ.get('CLIENT_SECRET'),
    solo_username=environ.get('SOLO_USERNAME'),
    solo_password=environ.get('SOLO_PASSWORD'),
    papi_domain_name=environ.get('PAPI_DOMAIN_NAME')
)
client.set_project_by_name(project_name)
project = client.project


def test_auth():
    assert client._papi_client is not None


def test_get_projects():
    assert not client.projects.to_df().empty


def test_get_project_wells():
    assert not project.wells.to_df().empty


def test_get_well():
    assert project.wells.find_by_name(well_name).to_df().at[0, 'name'] == well_name


def test_get_well_interpretation():
    interpretation = project.wells.find_by_name(well_name).interpretations.find_by_name(interpretation_name)
    assert interpretation.to_df()['meta'].at[0, 'name'] == interpretation_name


def test_get_well_starred_interpretation():
    interpretation = project.wells.find_by_name(well_name).starred_interpretation
    assert interpretation.to_df()['meta'].at[0, 'name'] == interpretation_name


def test_get_well_target_line():
    target_line = project.wells.find_by_name(well_name).target_lines.find_by_name(target_line_name)
    assert target_line.to_df().at[0, 'name'] == target_line_name


def test_get_well_starred_target_line():
    target_line = project.wells.find_by_name(well_name).starred_target_line
    assert target_line.to_df().at[0, 'name'] == target_line_name


def test_get_well_trajectory():
    trajectory = project.wells.find_by_name(well_name).trajectory

    assert not trajectory.to_df().empty
    assert trajectory.to_dict()


def test_get_well_trajectory_point():
    trajectory = project.wells.find_by_name(well_name).trajectory

    assert trajectory.find_by_md(0) is not None


def test_get_well_nested_wells():
    assert not project.wells.find_by_name(well_name).nested_wells.to_df().empty


def test_get_well_nested_well():
    well = project.wells.find_by_name(well_name)
    nested_well = well.nested_wells.find_by_name(nested_well_name)
    assert nested_well.to_df().at[0, 'name'] == nested_well_name


def test_create_nested_well():
    well = project.wells.find_by_name(well_name)
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
