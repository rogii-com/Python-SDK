import base64
import hashlib
import uuid
from typing import Any, Callable
from urllib.parse import urljoin, urlparse

import pandas as pd

from rogii_solo import __version__
from rogii_solo.papi.base import PapiClient as SdkPapiClient
from rogii_solo.papi.types import (
    PapiData,
    PapiDataIterator,
    PapiDataList,
    PapiStarredHorizons,
    PapiStarredTops,
    PapiVar,
    ProxyData,
    SettingsAuth,
)
from rogii_solo.utils.constants import (
    PYTHON_SDK_APP_ID,
    SOLO_OPEN_AUTH_SERVICE_URL,
    SOLO_PAPI_URL,
)


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
            headers=headers,
            proxies=self._get_proxies(settings_auth.proxies),
        )

    def _get_proxies(self, proxies_data: ProxyData) -> ProxyData:
        proxies: ProxyData = {}

        if not proxies_data:
            return proxies

        for scheme, url in proxies_data.items():
            if self._is_correct_proxy_url(url):
                proxies[scheme] = url

        return proxies

    def _is_correct_proxy_url(self, url: str) -> bool:
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ['https', 'http']:
            return False

        if not isinstance(parsed_url.port, int):
            return False

        return True

    def prepare_papi_var(self, value: float) -> PapiVar:
        """
        Create value dict for PAPI
        :param value:
        :return:
        """
        if isinstance(value, str):
            return value

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
        return list(self._gen_data_page(func=self.fetch_projects, **kwargs))

    def get_virtual_projects_data(self, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_virtual_projects, **kwargs))

    def get_project_wells_data(self, project_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_project_raw_wells, project_id=project_id, **kwargs))

    def get_project_well_data(self, well_id: str, **kwargs) -> PapiData:
        return self.parse_papi_data(self.fetch_raw_well(well_id=well_id, **kwargs))

    def get_well_trajectory_data(self, well_id: str, **kwargs) -> PapiDataList:
        return [
            self.parse_papi_data(data_item) for data_item in self.fetch_well_raw_trajectory(well_id=well_id, **kwargs)
        ]

    def get_well_interpretations_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_well_raw_interpretations, well_id=well_id, **kwargs))

    def get_interpretation_horizons_data(self, interpretation_id: str, **kwargs) -> PapiDataList:
        return list(
            self._gen_data_page(func=self.fetch_interpretation_horizons, interpretation_id=interpretation_id, **kwargs)
        )

    def get_interpretation_earth_models_data(self, interpretation_id: str, **kwargs) -> PapiDataList:
        return list(
            self._gen_data_page(
                func=self.fetch_interpretation_earth_models, interpretation_id=interpretation_id, **kwargs
            )
        )

    def get_interpretation_tvt_data(self, interpretation_id: str, **kwargs) -> PapiDataList:
        return [
            self.parse_papi_data(tvt_data)
            for tvt_data in self.fetch_interpretation_horizons_data(interpretation_id=interpretation_id, **kwargs)
        ]

    def get_interpretation_assembled_segments_data(self, interpretation_id: str, **kwargs) -> PapiData:
        assembled_segments = self.fetch_interpretation_assembled_segments(interpretation_id=interpretation_id, **kwargs)

        return {
            'horizons': self.parse_papi_data(assembled_segments['horizons']),
            'segments': self.parse_papi_data(assembled_segments['segments']),
        }

    def get_interpretation_starred_horizons(self, interpretation_id: str, **kwargs) -> PapiStarredHorizons:
        starred_horizons = self.fetch_interpretation_starred_horizons(interpretation_id=interpretation_id, **kwargs)

        return PapiStarredHorizons(
            top=starred_horizons['top'], center=starred_horizons['center'], bottom=starred_horizons['bottom']
        )

    def get_well_target_lines_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_well_target_lines, well_id=well_id, **kwargs))

    def get_well_nested_wells_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_well_nested_wells, well_id=well_id, **kwargs))

    def get_nested_well_trajectory_data(self, nested_well_id: str, **kwargs) -> PapiDataList:
        return [
            self.parse_papi_data(data_item)
            for data_item in self.fetch_nested_well_raw_trajectory(nested_well_id=nested_well_id, **kwargs)
        ]

    def get_well_logs_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_well_logs, well_id=well_id, **kwargs))

    def get_typewell_logs_data(self, typewell_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_typewell_logs, typewell_id=typewell_id, **kwargs))

    def get_log_points(self, log_id: str) -> PapiDataList:
        return [self.parse_papi_data(data_item) for data_item in self.fetch_log_points(log_id=log_id)]

    def get_project_typewells_data(self, project_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_project_typewells, project_id=project_id, **kwargs))

    def get_typewell_trajectory_data(self, typewell_id: str, **kwargs) -> PapiDataList:
        return [
            self.parse_papi_data(data_item)
            for data_item in self.fetch_typewell_raw_trajectory(typewell_id=typewell_id, **kwargs)
        ]

    def get_well_topsets_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_well_topsets, well_id=well_id, **kwargs))

    def get_typewell_topsets_data(self, typewell_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_typewell_topsets, typewell_id=typewell_id, **kwargs))

    def get_nested_well_topsets_data(self, nested_well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_nested_well_topsets, nested_well_id=nested_well_id, **kwargs))

    def get_topset_tops_data(self, topset_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_topset_tops, topset_id=topset_id, **kwargs))

    def get_topset_starred_tops(self, topset_id: str, **kwargs) -> PapiStarredTops:
        starred_tops = self.fetch_topset_starred_tops(topset_id=topset_id, **kwargs)

        return PapiStarredTops(top=starred_tops['top'], center=starred_tops['center'], bottom=starred_tops['bottom'])

    def get_well_mudlogs_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_well_mudlogs, well_id=well_id, **kwargs))

    def get_typewell_mudlogs_data(self, typewell_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_typewell_mudlogs, typewell_id=typewell_id, **kwargs))

    def get_mudlog_data(self, mudlog_id: str) -> PapiDataList:
        return [self.parse_papi_data(data_item) for data_item in self.fetch_mudlog_logs(mudlog_id)]

    def get_traces(self, **kwargs) -> PapiDataList:
        return self.fetch_traces(**kwargs)

    def get_well_mapped_time_traces_data(self, well_id: str, **kwargs) -> PapiDataList:
        return self.fetch_well_mapped_time_traces(well_id=well_id, **kwargs)

    # TODO Change to default _gen_data_page when offset will be added to the endpoint
    def get_well_time_trace_data(self, well_id: str, trace_id: str, **kwargs) -> PapiDataList:
        def _gen_data_page() -> PapiDataIterator:
            time_from = None
            limit = 500_000

            while True:
                data_page = self.fetch_well_time_trace(
                    well_id=well_id, trace_id=trace_id, time_from=time_from, limit=limit, **kwargs
                )

                for data_item in data_page:
                    yield self.parse_papi_data(data_item)

                if len(data_page) == 1:
                    break

                time_from = data_page[-1]['index']

        # Last data item on a page equals the first one on the next page, so we need to remove duplicates
        return pd.DataFrame(list(_gen_data_page())).drop_duplicates().to_dict('records')

    def get_well_mapped_calc_traces_data(self, well_id: str, **kwargs) -> PapiDataList:
        return self.fetch_well_mapped_calc_traces(well_id=well_id, **kwargs)

    def get_well_calc_trace_data(self, well_id: str, trace_id: str, **kwargs) -> PapiDataList:
        return self.fetch_well_calc_trace(well_id=well_id, trace_id=trace_id, **kwargs)

    def get_well_linked_typewells_data(self, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_well_linked_typewells, **kwargs))

    def get_well_comments_data(self, well_id: str, **kwargs) -> PapiDataList:
        return list(self._gen_data_page(func=self.fetch_well_comments, well_id=well_id, **kwargs))

    def get_well_attributes(self, well_id: str, **kwargs) -> PapiData:
        return self.parse_papi_data(self.fetch_well_attributes(well_id=well_id, **kwargs))

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
