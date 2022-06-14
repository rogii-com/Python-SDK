from functools import wraps
from typing import Any

from pandas import DataFrame

from .exceptions import ProjectNotFound, ProjectNotSelected
from .models import SettingsAuth
from .papi import PapiClient
from .utils.constants import SOLO_PAPI_DEFAULT_DOMAIN_NAME
from .utils.objects import find_by_key, find_by_path, is_data_dict, prepare_papi_var, to_pandas_dataframe


def python_sdk_project_checker(method):
    @wraps(method)
    def wrapped(*args, **kwargs):
        if not args[0]._project:
            raise ProjectNotSelected('Project is not selected.')

        return method(*args, **kwargs)

    return wrapped


class PyRogii:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 solo_username: str,
                 solo_password: str,
                 papi_domain_name: str = SOLO_PAPI_DEFAULT_DOMAIN_NAME
                 ):
        self._papi_client = PapiClient(
            SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                solo_username=solo_username,
                solo_password=solo_password,
                papi_domain_name=papi_domain_name
            )
        )
        self._project = None

    def set_project(self, project_name: str):
        projects = self._fetch_projects(project_filter=project_name)
        self._project = find_by_key(key='name', value=project_name, input_list=projects)

        if not self._project:
            raise ProjectNotFound('Project not found.')

    def get_projects(self, project_filter: str = None) -> DataFrame:
        projects = self._fetch_projects(project_filter=project_filter)
        parsed_projects = [self._parse_dict(item) for item in projects]

        return to_pandas_dataframe(parsed_projects)

    @python_sdk_project_checker
    def get_project_wells(self,  well_filter: str = None):
        project_wells = _request_all_pages_with_content(
            func=self._papi_client.fetch_project_wells,
            project_uuid=self._project['uuid'],
            well_filter=well_filter
        )
        return to_pandas_dataframe([self._parse_dict(item) for item in project_wells])

    @python_sdk_project_checker
    def get_well(self, well_name: str):
        well = self._fetch_well(well_name=well_name)

        if not well:
            return None

        return to_pandas_dataframe([self._parse_dict(well)])

    @python_sdk_project_checker
    def get_well_trajectory(self, well_name: str):
        well_uuid = self._find_well_uuid(well_name=well_name)

        if not well_uuid:
            return None

        well_raw_trajectory = self._papi_client.fetch_well_raw_trajectory(well_uuid=well_uuid)

        if not well_raw_trajectory:
            return None

        return to_pandas_dataframe([self._parse_dict(d) for d in well_raw_trajectory])

    @python_sdk_project_checker
    def get_well_interpretation(self, well_name: str, interpretation_name: str):
        well_uuid = self._find_well_uuid(well_name=well_name)

        if not well_uuid:
            return None

        interpretations = _request_all_pages(
            func=self._papi_client.fetch_well_raw_interpretations, well_uuid=well_uuid
        )
        interpretation = find_by_key(key='name', value=interpretation_name, input_list=interpretations)

        if not interpretation:
            return None

        return self._get_interpretation_data(interpretation=interpretation)

    @python_sdk_project_checker
    def get_well_starred_interpretation(self, well_name: str):
        well = self._fetch_well(well_name=well_name)
        starred_interpretation_uuid = find_by_path(well, 'starred.interpretation')

        if not starred_interpretation_uuid:
            return None

        interpretations = _request_all_pages(
            func=self._papi_client.fetch_well_raw_interpretations, well_uuid=well['uuid']
        )
        starred_interpretation = find_by_key(
            key='uuid', value=starred_interpretation_uuid, input_list=interpretations
        )

        return self._get_interpretation_data(interpretation=starred_interpretation)

    @python_sdk_project_checker
    def get_well_target_lines(self, well_name: str):
        target_lines = self._fetch_well_target_lines(well_name=well_name)

        if not target_lines:
            return None

        return to_pandas_dataframe([self._parse_dict(item) for item in target_lines])

    @python_sdk_project_checker
    def get_well_target_line(self, well_name: str, target_line_name: str):
        target_lines = self._fetch_well_target_lines(well_name=well_name)
        target_line = find_by_key(key='name', value=target_line_name, input_list=target_lines)

        if not target_line:
            return None

        return to_pandas_dataframe([self._parse_dict(target_line)])

    @python_sdk_project_checker
    def get_well_starred_target_line(self, well_name: str):
        well = self._fetch_well(well_name)
        starred_target_line_uuid = find_by_path(well, 'starred.target_line')
        target_lines = self._fetch_well_target_lines(well_name=well_name)
        target_line = find_by_key(key='uuid', value=starred_target_line_uuid, input_list=target_lines)

        if not target_line:
            return None

        return to_pandas_dataframe([self._parse_dict(target_line)])

    @python_sdk_project_checker
    def create_nested_well(self,
                           well_name: str,
                           nested_well_name: str,
                           operator: str,
                           api: str,
                           xsrf: float,
                           ysrf: float,
                           kb: float,
                           tie_in_tvd: float,
                           tie_in_ns: float,
                           tie_in_ew: float
                           ):
        well_uuid = self._find_well_uuid(well_name=well_name)

        if not well_uuid:
            return None

        return self._papi_client.create_nested_well(
            well_uuid=well_uuid,
            nested_well_name=nested_well_name,
            operator=operator,
            api=api,
            xsrf=prepare_papi_var(xsrf),
            ysrf=prepare_papi_var(ysrf),
            kb=prepare_papi_var(kb),
            tie_in_tvd=prepare_papi_var(tie_in_tvd),
            tie_in_ns=prepare_papi_var(tie_in_ns),
            tie_in_ew=prepare_papi_var(tie_in_ew)
        )

    @python_sdk_project_checker
    def replace_nested_well_trajectory(self,
                                       well_name: str,
                                       md_uom: str,
                                       incl_uom: str,
                                       azi_uom: str,
                                       trajectory_stations: list
                                       ):
        well_uuid = self._find_well_uuid(well_name=well_name)

        if not well_uuid:
            return None

        wrapped_trajectory_stations = [
            {key: prepare_papi_var(value) for key, value in point.items()}
            for point in trajectory_stations
        ]

        # FIXME: temporary fix for SOLO-5351
        fixed_wrapped_trajectory_stations = [
            {key if key != 'azim' else 'azi': value for key, value in point.items()}
            for point in wrapped_trajectory_stations
        ]

        return self._papi_client.replace_nested_well_trajectory(
            well_uuid=well_uuid,
            md_uom=md_uom,
            incl_uom=incl_uom,
            azi_uom=azi_uom,
            trajectory_stations=fixed_wrapped_trajectory_stations
        )

    @python_sdk_project_checker
    def get_well_nested_wells(self, well_name: str):
        nested_wells = self._fetch_well_nested_wells(well_name=well_name)

        if not nested_wells:
            return None

        return to_pandas_dataframe([self._parse_dict(item) for item in nested_wells])

    @python_sdk_project_checker
    def get_well_nested_well(self, well_name: str, nested_well_name: str):
        nested_wells = self._fetch_well_nested_wells(well_name=well_name)
        nested_well = find_by_key(key='name', value=nested_well_name, input_list=nested_wells)

        if not nested_well:
            return None

        return to_pandas_dataframe([self._parse_dict(nested_well)])

    def _parse_dict(self, obj: Any, default: Any = None) -> Any:
        """
        Recursive dictionary parsing. Its elements can be either of the regular type values,
        list/dictionary, or dictionaries with "val" or "undefined" key
        """
        # TODO: The method parses only dict() and list() from complex types and no other complex types
        if isinstance(obj, dict):
            if is_data_dict(obj):
                return obj['val'] if 'val' in obj else default
            else:
                return {item: self._parse_dict(value) for item, value in obj.items()}
        elif isinstance(obj, list):
            return [self._parse_dict(item) for item in obj]
        else:
            return obj

    def _fetch_projects(self, project_filter: str = None) -> list:
        return _request_all_pages_with_content(
            func=self._papi_client.fetch_projects,
            project_filter=project_filter
        )

    def _find_well_uuid(self, well_name: str):
        wells = _request_all_pages_with_content(
            func=self._papi_client.fetch_project_wells,
            project_uuid=self._project['uuid']
        )

        return find_by_key(
            input_list=wells, key='name', value=well_name
        ).get('uuid', None)

    def _fetch_well(self, well_name: str):
        well_uuid = self._find_well_uuid(well_name=well_name)

        if not well_uuid:
            return None

        return self._papi_client.fetch_raw_well(well_uuid=well_uuid)

    def _fetch_well_target_lines(self, well_name: str):
        well_uuid = self._find_well_uuid(well_name=well_name)

        if not well_uuid:
            return None

        return _request_all_pages_with_content(
            func=self._papi_client.fetch_well_target_lines,
            well_uuid=well_uuid
        )

    def _fetch_well_nested_wells(self, well_name: str):
        well_uuid = self._find_well_uuid(well_name=well_name)

        if not well_uuid:
            return None

        return _request_all_pages_with_content(
            func=self._papi_client.fetch_well_nested_wells,
            well_uuid=well_uuid
        )

    def _get_interpretation_data(self, interpretation: dict):
        assembled_segments = self._papi_client.fetch_well_interpretation_assembled_segments(
            well_interpretation_uuid=interpretation['uuid']
        )

        horizons = _request_all_pages(
            func=self._papi_client.fetch_well_interpretation_horizons,
            well_interpretation_uuid=interpretation['uuid']
        )
        for horizon in horizons:
            assembled_segments['horizons'][horizon['uuid']]['name'] = horizon['name']

        return {
            'meta': to_pandas_dataframe([interpretation]),
            'horizons': DataFrame(self._parse_dict(assembled_segments['horizons'])).transpose(),
            'segments': to_pandas_dataframe(self._parse_dict(assembled_segments['segments']))
        }


def _request_all_pages_with_content(func, **kwarg):
    result = []
    offset = PapiClient.DEFAULT_OFFSET
    last = False

    while not last:
        request = func(offset=offset, **kwarg)
        result.extend(request['content'])
        offset += PapiClient.DEFAULT_LIMIT
        last = request['last']

    return result


def _request_all_pages(func, **kwarg):
    result = []
    offset = PapiClient.DEFAULT_OFFSET

    while True:
        request = func(offset=offset, **kwarg)
        if not len(request):
            break
        result.extend(request)
        offset += PapiClient.DEFAULT_LIMIT

    return result
