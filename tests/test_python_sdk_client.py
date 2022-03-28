from os import environ

from python_sdk.client import PyRogii


pr = PyRogii(
    client_id=environ.get("CLIENT_ID"),
    client_secret=environ.get("CLIENT_SECRET"),
    solo_username=environ.get("SOLO_USERNAME"),
    solo_password=environ.get("SOLO_PASSWORD"),
    papi_domain_name=environ.get("PAPI_DOMAIN_NAME")
)

def test_auth():
    assert pr.fetch_projects(project_filter="python_sdk")['total'] == 1

