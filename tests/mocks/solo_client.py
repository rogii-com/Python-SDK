from rogii_solo.client import SoloClient

from tests.mocks.papi_data import (
    PROJECTS_DATA_RESPONSE,
    VIRTUAL_PROJECTS_DATA_RESPONSE,
    WELLS_DATA_RESPONSE,
    TRAJECTORY_DATA_RESPONSE,
    INTERPRETATIONS_DATA_RESPONSE,
    HORIZONS_DATA_RESPONSE,
    ASSEMBLED_SEGMENTS_DATA_RESPONSE,
    TARGET_LINES_DATA_RESPONSE,
    NESTED_WELLS_DATA_RESPONSE
)


def fetch_well_raw_trajectory(**kwargs):
    return TRAJECTORY_DATA_RESPONSE['content']


def fetch_interpretation_assembled_segments(**kwargs):
    return ASSEMBLED_SEGMENTS_DATA_RESPONSE['assembled_segments']


solo_client = SoloClient(client_id='client_id', client_secret='client_secret')

solo_client._papi_client.fetch_projects = lambda **kwargs: PROJECTS_DATA_RESPONSE
solo_client._papi_client.fetch_virtual_projects = lambda **kwargs: VIRTUAL_PROJECTS_DATA_RESPONSE
solo_client._papi_client.fetch_project_wells = lambda **kwargs: WELLS_DATA_RESPONSE
solo_client._papi_client.fetch_well_raw_trajectory = fetch_well_raw_trajectory
solo_client._papi_client.fetch_well_raw_interpretations = lambda **kwargs: INTERPRETATIONS_DATA_RESPONSE
solo_client._papi_client.fetch_interpretation_horizons = lambda **kwargs: HORIZONS_DATA_RESPONSE
solo_client._papi_client.fetch_interpretation_assembled_segments = fetch_interpretation_assembled_segments
solo_client._papi_client.fetch_well_target_lines = lambda **kwargs: TARGET_LINES_DATA_RESPONSE
solo_client._papi_client.fetch_well_nested_wells = lambda **kwargs: NESTED_WELLS_DATA_RESPONSE
