import random
from os import environ

from python_sdk.client import PyRogii, to_pandas_dataframe

project_name = 'nsapegin (ft)'
well_name = 'Lateral1'
interpretation_name = 'Interpretation1'
target_line_name = 'Target Line1'
nested_well_name = 'Nested Well'

pr = PyRogii(
    client_id=environ.get('CLIENT_ID'),
    client_secret=environ.get('CLIENT_SECRET'),
    solo_username=environ.get('SOLO_USERNAME'),
    solo_password=environ.get('SOLO_PASSWORD'),
    papi_domain_name=environ.get('PAPI_DOMAIN_NAME')
)
pr.set_project(project_name)


def test_auth():
    assert pr._papi_client is not None


def test_to_pandas_dataframe():
    df = to_pandas_dataframe(
            [{
                'name': 'Lateral one',
                'uuid': '8b691de9-775f-4638-a330-d6deb5a3dc50',
                'api': 'api nested well one'
            }],
    )
    assert df['name'][0] == 'Lateral one'


def test_get_projects():
    assert not pr.get_projects(project_filter=project_name).empty


def test_get_project_wells():
    assert not pr.get_project_wells().empty


def test_get_well():
    assert pr.get_well(well_name=well_name).at[0, 'name'] == well_name


def test_get_well_interpretation():
    interpretation = pr.get_well_interpretation(well_name=well_name, interpretation_name=interpretation_name)
    assert interpretation['meta'].at[0, 'name'] == interpretation_name


def test_get_well_starred_interpretation():
    interpretation = pr.get_well_starred_interpretation(well_name=well_name)
    assert interpretation['meta'].at[0, 'name'] == interpretation_name


def test_get_well_target_line():
    target_line = pr.get_well_target_line(well_name=well_name, target_line_name=target_line_name)
    assert target_line.at[0, 'name'] == target_line_name


def test_get_well_starred_target_line():
    target_line = pr.get_well_starred_target_line(well_name=well_name)
    assert target_line.at[0, 'name'] == target_line_name


def test_get_well_target_lines():
    assert not pr.get_well_target_lines(well_name=well_name).empty


def test_get_well_trajectory():
    assert not pr.get_well_trajectory(well_name=well_name).empty


def test_get_well_nested_wells():
    assert not pr.get_well_nested_wells(well_name=well_name).empty


def test_get_well_nested_well():
    nested_well = pr.get_well_nested_well(well_name=well_name, nested_well_name=nested_well_name)
    assert nested_well.at[0, 'name'] == nested_well_name


def test_create_nested_well():
    nested_well_name = 'Nested Well ' + str(random.randint(0, 10000))
    pr.create_nested_well(
        well_name=well_name,
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
    assert pr.get_well_nested_well(well_name=well_name, nested_well_name=nested_well_name) is not None
