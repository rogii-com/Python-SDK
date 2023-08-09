from os import environ

import pytest

from rogii_solo import SoloClient
from tests.papi_data import (
    ABSENT_HORIZONS_DATA_RESPONSE,
    ASSEMBLED_SEGMENTS_DATA_RESPONSE,
    ASSEMBLED_SEGMENTS_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_DATA_RESPONSE,
    ASSEMBLED_SEGMENTS_LAST_SEGMENT_ONE_POINT_DATA_RESPONSE,
    CALC_TRACE_DATA_RESPONSE,
    COMMENTS_DATA_RESPONSE,
    EARTH_MODEL_SECTIONS_DATA_RESPONSE,
    EARTH_MODELS_DATA_RESPONSE,
    EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ASSEMBLED_SEGMENTS_DATA_RESPONSE,
    EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ID,
    EI_ALL_SEGMENTS_OUT_ASSEMBLED_SEGMENTS_DATA_RESPONSE,
    EI_ALL_SEGMENTS_OUT_ID,
    EI_LAST_SEGMENT_EXTENDED_ASSEMBLED_SEGMENTS_DATA_RESPONSE,
    EI_LAST_SEGMENT_EXTENDED_ID,
    EI_LAST_SEGMENT_OUT_ASSEMBLED_SEGMENTS_DATA_RESPONSE,
    EI_LAST_SEGMENT_OUT_ID,
    FOOT_METER_PROJECT_NAME,
    FOOT_PROJECT_NAME,
    HORIZONS_DATA_RESPONSE,
    HORIZONS_TVT_DATA_RESPONSE,
    INTERPRETATION_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_ID,
    INTERPRETATION_LAST_SEGMENT_ONE_POINT_ID,
    INTERPRETATIONS_DATA_RESPONSE,
    LOG_POINTS_DATA_RESPONSE,
    LOGS_DATA_RESPONSE,
    MAPPED_CALC_TRACES_DATA_RESPONSE,
    MAPPED_TIME_TRACES_DATA_RESPONSE,
    METER_PROJECT_NAME,
    MUDLOG_DATA_RESPONSE,
    MUDLOGS_DATA_RESPONSE,
    NESTED_WELLS_DATA_RESPONSE,
    PROJECTS_DATA_RESPONSE,
    STARRED_HORIZONS_DATA_RESPONSE,
    STARRED_TOPS_DATA_RESPONSE,
    TARGET_LINES_DATA_RESPONSE,
    TIME_TRACE_DATA_RESPONSE,
    TOPS_DATA_RESPONSE,
    TOPSETS_DATA_RESPONSE,
    TRACES_DATA_RESPONSE,
    TRAJECTORY_DATA_RESPONSE,
    TYPEWELLS_DATA_RESPONSE,
    VIRTUAL_PROJECTS_DATA_RESPONSE,
    WELL_ATTRIBUTES_DATA_RESPONSE,
    WELL_LINKED_TYPEWELLS_DATA_RESPONSE,
    WELLS_DATA_RESPONSE,
)


def fetch_projects(**kwargs):
    return PROJECTS_DATA_RESPONSE


def fetch_virtual_projects(**kwargs):
    return VIRTUAL_PROJECTS_DATA_RESPONSE


def fetch_project_raw_wells(**kwargs):
    return WELLS_DATA_RESPONSE


def fetch_well_raw_trajectory(**kwargs):
    return TRAJECTORY_DATA_RESPONSE['content']


def fetch_well_raw_interpretations(**kwargs):
    return INTERPRETATIONS_DATA_RESPONSE


def fetch_interpretation_horizons(**kwargs):
    if kwargs['interpretation_id'] == EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ID:
        return ABSENT_HORIZONS_DATA_RESPONSE
    elif kwargs['interpretation_id'] == INTERPRETATION_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_ID:
        return ABSENT_HORIZONS_DATA_RESPONSE

    return HORIZONS_DATA_RESPONSE


def fetch_interpretation_assembled_segments(**kwargs):
    if kwargs['interpretation_id'] == EI_LAST_SEGMENT_EXTENDED_ID:
        return EI_LAST_SEGMENT_EXTENDED_ASSEMBLED_SEGMENTS_DATA_RESPONSE['assembled_segments']
    elif kwargs['interpretation_id'] == EI_LAST_SEGMENT_OUT_ID:
        return EI_LAST_SEGMENT_OUT_ASSEMBLED_SEGMENTS_DATA_RESPONSE['assembled_segments']
    elif kwargs['interpretation_id'] == EI_ALL_SEGMENTS_OUT_ID:
        return EI_ALL_SEGMENTS_OUT_ASSEMBLED_SEGMENTS_DATA_RESPONSE['assembled_segments']
    elif kwargs['interpretation_id'] == EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ID:
        return EI_ABSENT_HORIZONS_LAST_SEGMENT_OUT_ASSEMBLED_SEGMENTS_DATA_RESPONSE['assembled_segments']
    elif kwargs['interpretation_id'] == INTERPRETATION_LAST_SEGMENT_ONE_POINT_ID:
        return ASSEMBLED_SEGMENTS_LAST_SEGMENT_ONE_POINT_DATA_RESPONSE['assembled_segments']
    elif kwargs['interpretation_id'] == INTERPRETATION_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_ID:
        return ASSEMBLED_SEGMENTS_LAST_SEGMENT_ONE_POINT_ABSENT_HORIZONS_DATA_RESPONSE['assembled_segments']

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


def fetch_project_typewells(**kwargs):
    return TYPEWELLS_DATA_RESPONSE


def fetch_typewell_raw_trajectory(**kwargs):
    return TRAJECTORY_DATA_RESPONSE['content']


def fetch_well_topsets(**kwargs):
    return TOPSETS_DATA_RESPONSE


def fetch_topset_tops(**kwargs):
    return TOPS_DATA_RESPONSE


def fetch_interpretation_starred_horizons(**kwargs):
    return STARRED_HORIZONS_DATA_RESPONSE


def fetch_topset_starred_tops(**kwargs):
    return STARRED_TOPS_DATA_RESPONSE


def fetch_well_mudlogs(**kwargs):
    return MUDLOGS_DATA_RESPONSE


def fetch_mudlog_logs(*args, **kwargs):
    return MUDLOG_DATA_RESPONSE['logs']


def fetch_traces(**kwargs):
    return TRACES_DATA_RESPONSE['content']


def fetch_well_mapped_time_traces(**kwargs):
    return MAPPED_TIME_TRACES_DATA_RESPONSE['content']


def fetch_well_time_trace(**kwargs):
    return TIME_TRACE_DATA_RESPONSE['content']


def fetch_well_mapped_calc_traces(**kwargs):
    return MAPPED_CALC_TRACES_DATA_RESPONSE['content']


def fetch_well_calc_trace(**kwargs):
    return CALC_TRACE_DATA_RESPONSE['content']


def get_well_time_trace_data(**kwargs):
    return TIME_TRACE_DATA_RESPONSE['content']


def fetch_well_linked_typewells(**kwargs):
    return WELL_LINKED_TYPEWELLS_DATA_RESPONSE


def fetch_well_comments(**kwargs):
    return COMMENTS_DATA_RESPONSE


def fetch_well_attributes(**kwargs):
    return WELL_ATTRIBUTES_DATA_RESPONSE


def fetch_interpretation_earth_models(**kwargs):
    return EARTH_MODELS_DATA_RESPONSE


def fetch_earth_model_sections(**kwargs):
    return EARTH_MODEL_SECTIONS_DATA_RESPONSE


@pytest.fixture(scope='function')
def solo_client():
    solo_client = SoloClient(client_id='client_id', client_secret='client_secret')

    solo_client._papi_client.fetch_projects = fetch_projects
    solo_client._papi_client.fetch_virtual_projects = fetch_virtual_projects
    solo_client._papi_client.fetch_project_raw_wells = fetch_project_raw_wells
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
    solo_client._papi_client.fetch_project_typewells = fetch_project_typewells
    solo_client._papi_client.fetch_typewell_raw_trajectory = fetch_typewell_raw_trajectory
    solo_client._papi_client.fetch_well_topsets = fetch_well_topsets
    solo_client._papi_client.fetch_topset_tops = fetch_topset_tops
    solo_client._papi_client.fetch_interpretation_starred_horizons = fetch_interpretation_starred_horizons
    solo_client._papi_client.fetch_topset_starred_tops = fetch_topset_starred_tops
    solo_client._papi_client.fetch_well_mudlogs = fetch_well_mudlogs
    solo_client._papi_client.fetch_mudlog_logs = fetch_mudlog_logs
    solo_client._papi_client.fetch_traces = fetch_traces
    solo_client._papi_client.fetch_well_mapped_time_traces = fetch_well_mapped_time_traces
    solo_client._papi_client.fetch_well_mapped_calc_traces = fetch_well_mapped_calc_traces
    solo_client._papi_client.fetch_well_time_trace = fetch_well_time_trace
    solo_client._papi_client.fetch_well_calc_trace = fetch_well_calc_trace
    solo_client._papi_client.get_well_time_trace_data = get_well_time_trace_data
    solo_client._papi_client.fetch_well_linked_typewells = fetch_well_linked_typewells
    solo_client._papi_client.fetch_well_comments = fetch_well_comments
    solo_client._papi_client.fetch_well_attributes = fetch_well_attributes
    solo_client._papi_client.fetch_interpretation_earth_models = fetch_interpretation_earth_models
    solo_client._papi_client.fetch_earth_model_sections = fetch_earth_model_sections

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
        papi_domain_name=environ.get('ROGII_SOLO_PAPI_DOMAIN_NAME'),
    )

    return papi_solo_client


@pytest.fixture(scope='module')
def project_papi(solo_client_papi):
    solo_client_papi.set_project_by_name(environ.get('ROGII_SOLO_PROJECT_NAME'))

    return solo_client_papi.project
