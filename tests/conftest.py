from os import environ
import pytest

from rogii_solo import SoloClient
from tests.papi_data import (
    METER_PROJECT_NAME,
    FOOT_PROJECT_NAME,
    FOOT_METER_PROJECT_NAME,
    PROJECTS_DATA_RESPONSE,
    VIRTUAL_PROJECTS_DATA_RESPONSE,
    WELLS_DATA_RESPONSE,
    TRAJECTORY_DATA_RESPONSE,
    INTERPRETATIONS_DATA_RESPONSE,
    HORIZONS_DATA_RESPONSE,
    ASSEMBLED_SEGMENTS_DATA_RESPONSE,
    TARGET_LINES_DATA_RESPONSE,
    NESTED_WELLS_DATA_RESPONSE,
    LOGS_DATA_RESPONSE,
    LOG_POINTS_DATA_RESPONSE,
    HORIZONS_TVT_DATA_RESPONSE
)


def fetch_projects(**kwargs):
    return PROJECTS_DATA_RESPONSE


def fetch_virtual_projects(**kwargs):
    return VIRTUAL_PROJECTS_DATA_RESPONSE


def fetch_project_wells(**kwargs):
    return WELLS_DATA_RESPONSE


def fetch_well_raw_trajectory(**kwargs):
    return TRAJECTORY_DATA_RESPONSE['content']


def fetch_well_raw_interpretations(**kwargs):
    return INTERPRETATIONS_DATA_RESPONSE


def fetch_interpretation_horizons(**kwargs):
    return HORIZONS_DATA_RESPONSE


def fetch_interpretation_assembled_segments(**kwargs):
    return ASSEMBLED_SEGMENTS_DATA_RESPONSE['assembled_segments']


def fetch_interpretation_horizons_data(**kwargs):
    return HORIZONS_TVT_DATA_RESPONSE['content']


def fetch_well_target_lines(**kwargs):
    return TARGET_LINES_DATA_RESPONSE


def fetch_well_nested_wells(**kwargs):
    return NESTED_WELLS_DATA_RESPONSE


def fetch_nested_well_raw_trajectory(**kwargs):
    return TRAJECTORY_DATA_RESPONSE['content']


def fetch_well_logs(**kwargs):
    return LOGS_DATA_RESPONSE


def fetch_log_points(**kwargs):
    return LOG_POINTS_DATA_RESPONSE['log_points']


@pytest.fixture(scope='function')
def solo_client():
    solo_client = SoloClient(client_id='client_id', client_secret='client_secret')

    solo_client._papi_client.fetch_projects = fetch_projects
    solo_client._papi_client.fetch_virtual_projects = fetch_virtual_projects
    solo_client._papi_client.fetch_project_wells = fetch_project_wells
    solo_client._papi_client.fetch_well_raw_trajectory = fetch_well_raw_trajectory
    solo_client._papi_client.fetch_well_raw_interpretations = fetch_well_raw_interpretations
    solo_client._papi_client.fetch_interpretation_horizons = fetch_interpretation_horizons
    solo_client._papi_client.fetch_interpretation_assembled_segments = fetch_interpretation_assembled_segments
    solo_client._papi_client.fetch_well_target_lines = fetch_well_target_lines
    solo_client._papi_client.fetch_well_nested_wells = fetch_well_nested_wells
    solo_client._papi_client.fetch_nested_well_raw_trajectory = fetch_nested_well_raw_trajectory
    solo_client._papi_client.fetch_well_logs = fetch_well_logs
    solo_client._papi_client.fetch_log_points = fetch_log_points
    solo_client._papi_client.fetch_interpretation_horizons_data = fetch_interpretation_horizons_data

    return solo_client


@pytest.fixture(scope='function')
def project(solo_client):
    solo_client.set_project_by_name(METER_PROJECT_NAME)

    return solo_client.project


@pytest.fixture(scope='function')
def ft_project(solo_client):
    solo_client.set_project_by_name(FOOT_PROJECT_NAME)

    return solo_client.project


@pytest.fixture(scope='function')
def ftm_project(solo_client):
    solo_client.set_project_by_name(FOOT_METER_PROJECT_NAME)

    return solo_client.project


@pytest.fixture(scope='module')
def solo_client_papi():
    papi_solo_client = SoloClient(
        client_id=environ.get('ROGII_SOLO_CLIENT_ID'),
        client_secret=environ.get('ROGII_SOLO_CLIENT_SECRET'),
        papi_domain_name=environ.get('ROGII_SOLO_PAPI_DOMAIN_NAME')
    )

    return papi_solo_client


@pytest.fixture(scope='module')
def project_papi(solo_client_papi):
    solo_client_papi.set_project_by_name(METER_PROJECT_NAME)

    return solo_client_papi.project
