import base64
import hashlib
import uuid
from typing import Any, Callable
from urllib.parse import urljoin

from rogii_solo import __version__
from rogii_solo.papi.base import PapiClient as SdkPapiClient
from rogii_solo.papi.types import PapiData, PapiDataIterator, PapiDataList, PapiVar, SettingsAuth
from rogii_solo.utils.constants import PYTHON_SDK_APP_ID, SOLO_OPEN_AUTH_SERVICE_URL, SOLO_PAPI_URL


class PapiClient(SdkPapiClient):
    def __init__(self, settings_auth: SettingsAuth):
        app_id = base64.standard_b64encode(PYTHON_SDK_APP_ID.encode()).decode()

        fingerprint = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
        headers = {
            'User-Agent': f'PythonSDK/{__version__}',
            'X-Solo-Hid': f'{fingerprint}:{app_id}',
        }

        papi_url = urljoin(settings_auth.papi_domain_name, SOLO_PAPI_URL)
        papi_auth_url = urljoin(settings_auth.papi_domain_name, SOLO_OPEN_AUTH_SERVICE_URL)

        super().__init__(
            papi_url=papi_url,
            papi_auth_url=papi_auth_url,
            papi_client_id=settings_auth.client_id,
            papi_client_secret=settings_auth.client_secret,
            headers=headers
        )

    def prepare_papi_var(self, value: float) -> PapiVar:
        """
        Create value dict for PAPI
        :param value:
        :return:
        """
        if value is None:
            return {'undefined': True}

        return {'val': value}

    def parse_papi_data(self, data: Any, default: Any = None) -> Any:
        """
        Recursive PAPI data parsing.
        Elements can be either of the regular type values, list/dict, or dicts with "val" or "undefined" key.
        """
        if isinstance(data, dict):
            if 'val' in data or 'undefined' in data:
                return data.get('val', default)
            else:
                return {item: self.parse_papi_data(value) for item, value in data.items()}
        elif isinstance(data, list):
            return [self.parse_papi_data(item) for item in data]
        else:
            return data

    def get_global_projects_data(self, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(
            func=self.fetch_projects,
            **kwargs
        ))

    def get_virtual_projects_data(self, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(
            func=self.fetch_virtual_projects,
            **kwargs
        ))

    def get_project_wells_data(self, project_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(
            func=self.fetch_project_wells,
            project_id=project_id,
            **kwargs
        ))

    def get_well_trajectory_data(self, well_id: str, **kwargs) -> PapiDataList:
        return [
            self.parse_papi_data(data_item) for data_item in self.fetch_well_raw_trajectory(
                well_id=well_id,
                **kwargs
            )
        ]

    def get_well_interpretations_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(
            func=self.fetch_well_raw_interpretations,
            well_id=well_id,
            **kwargs
        ))

    def get_interpretation_horizons_data(self, interpretation_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(
            func=self.fetch_interpretation_horizons,
            interpretation_id=interpretation_id,
            **kwargs
        ))

    def get_interpretation_tvt_data(self, interpretation_id: str, **kwargs) -> PapiDataList:
        return [
            self.parse_papi_data(tvt_data) for tvt_data in self.fetch_interpretation_horizons_data(
                interpretation_id=interpretation_id,
                **kwargs
            )
        ]

    def get_interpretation_assembled_segments_data(self, interpretation_id: str, **kwargs) -> PapiData:
        assembled_segments = self.fetch_interpretation_assembled_segments(
            interpretation_id=interpretation_id,
            **kwargs
        )

        return {
            'horizons': self.parse_papi_data(assembled_segments['horizons']),
            'segments': self.parse_papi_data(assembled_segments['segments']),
        }

    def get_well_target_lines_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(
            func=self.fetch_well_target_lines,
            well_id=well_id,
            **kwargs
        ))

    def get_well_nested_wells_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(
            func=self.fetch_well_nested_wells,
            well_id=well_id,
            **kwargs
        ))

    def get_nested_well_trajectory_data(self, nested_well_id: str, **kwargs) -> PapiDataList:
        return [
            self.parse_papi_data(data_item) for data_item in self.fetch_nested_well_raw_trajectory(
                nested_well_id=nested_well_id,
                **kwargs
            )
        ]

    def get_well_logs_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(
            func=self.fetch_well_logs,
            well_id=well_id,
            **kwargs
        ))

    def get_log_data(self, log_id: str) -> PapiDataList:
        return [
            self.parse_papi_data(data_item) for data_item in self.fetch_log_points(log_id=log_id)
        ]

    def _gen_data_page(self, func: Callable, **kwargs) -> PapiDataIterator:
        offset = kwargs.pop('offset', None) or self.DEFAULT_OFFSET
        limit = kwargs.pop('limit', None) or self.DEFAULT_LIMIT

        while True:
            response = func(offset=offset, limit=limit, **kwargs)

            for data_page in response.get('content', []):
                yield self.parse_papi_data(data_page)

            if response.get('last', True):
                break

            offset += limit
