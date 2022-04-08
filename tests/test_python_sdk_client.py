from os import environ

from python_sdk.client import PyRogii


pr = PyRogii(
    client_id=environ.get('CLIENT_ID'),
    client_secret=environ.get('CLIENT_SECRET'),
    solo_username=environ.get('SOLO_USERNAME'),
    solo_password=environ.get('SOLO_PASSWORD'),
    papi_domain_name=environ.get('PAPI_DOMAIN_NAME')
)


def test_auth():
    assert pr.papi_client is not None


def test_to_pandas_dataframe():
    df = pr.to_pandas_dataframe(
            [{
                'name': 'Lateral one',
                'uuid': '8b691de9-775f-4638-a330-d6deb5a3dc50',
                'api': 'api nested well one'
            }],
    )
    assert df['name'][0] == 'Lateral one'


def test_get_projects():
    assert not pr.get_projects(project_filter='python_sdk').empty


def test_get_well():
    assert not pr.get_well(well_uuid='05901b21-c94e-468e-99ab-78bf20aa345f').empty
