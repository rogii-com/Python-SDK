from typing import Any, Dict, List, Optional

from oauthlib.oauth2 import BackendApplicationClient, LegacyApplicationClient
from requests import codes as status_codes
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from rogii_solo.papi.exceptions import (
    AccessTokenFailureException,
    BasePapiClientException,
)
from rogii_solo.papi.types import (
    PapiLogPoint,
    PapiObjectCreationResult,
    PapiStarredHorizons,
    PapiStarredTops,
    PapiTrajectory,
    PapiVar,
    TraceType,
)


class BasePapiClient:
    DEFAULT_OFFSET = 0
    DEFAULT_LIMIT = 100
    LIMIT_MAX = 200
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(
        self,
        papi_url: str,
        papi_auth_url: str,
        papi_client_id: str,
        papi_client_secret: str,
        solo_username: str = None,
        solo_password: str = None,
        headers: Optional[Dict] = None,
        proxies: Optional[Dict] = None,
    ):
        self.papi_url = papi_url
        self.token_url = f'{papi_auth_url}/token'

        self.papi_client_id = papi_client_id
        self.papi_client_secret = papi_client_secret

        self.solo_username = solo_username
        self.solo_password = solo_password

        self.headers = headers or {}
        self.proxies = proxies or {}
        self._session = None

    @property
    def session(self):
        if not self._session:
            self._session = self._get_session()

        return self._session

    def _get_session(self):
        token_params = {
            'token_url': self.token_url,
            'client_id': self.papi_client_id,
            'client_secret': self.papi_client_secret,
            'auth': HTTPBasicAuth(self.papi_client_id, self.papi_client_secret),
            'headers': self.headers,
        }

        if self.solo_username and self.solo_password:
            client = LegacyApplicationClient(client_id=self.papi_client_id)

            token_params['username'] = self.solo_username
            token_params['password'] = self.solo_password
        else:
            client = BackendApplicationClient(client_id=self.papi_client_id)

        try:
            auth_session = OAuth2Session(client=client)
            auth_session.proxies.update(self.proxies)

            token_data = auth_session.fetch_token(**token_params)
        except Exception:
            raise AccessTokenFailureException(
                'Failed to get access token. Please check that your auth settings are correct.'
            )

        session = OAuth2Session(
            client=client, token=token_data, auto_refresh_url=self.token_url, token_updater=self._update_token_data
        )

        # "Client credentials" grant type does not support token refreshing
        if isinstance(session._client, BackendApplicationClient):
            session.refresh_token = lambda *args, **kwargs: session.fetch_token(**token_params)

        session.headers.update({'Authorization': f"Bearer {token_data['access_token']}"})
        session.headers.update(self.headers)
        session.proxies.update(self.proxies)

        # There no ability to add basic auth to the "refresh_token" method in requests_oauthlib.
        # "auto_refresh_kwargs" parameter can't be used for this either.
        session.refresh_token = self._wrap_with_auth(session.refresh_token)

        return session

    def _wrap_with_auth(self, func):
        def wrapper(*args, **kwargs):
            kwargs['auth'] = HTTPBasicAuth(self.papi_client_id, self.papi_client_secret)
            return func(*args, **kwargs)

        return wrapper

    def _update_token_data(self, token_data):
        self.session.headers.update({'Authorization': f"Bearer {token_data['access_token']}"})

    def _send_request(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None):
        response = self.session.get(f'{self.papi_url}/{url}', params=params, headers=headers)

        if response.status_code != status_codes.ok:
            error = response.json()
            raise BasePapiClientException(error)

        if response.text:
            return response.json()

        return response

    def _send_post_request(
        self, url: str, request_data: Dict[str, Any], params: Optional[Dict] = None, headers: Optional[Dict] = None
    ):
        response = self.session.post(f'{self.papi_url}/{url}', params=params, json=request_data, headers=headers)

        if response.status_code != status_codes.ok:
            error = response.json()
            raise BasePapiClientException(error)

        if response.text:
            return response.json()

        return response

    def _send_put_request(self, url: str, request_data: Dict[str, Any], headers: Optional[Dict] = None):
        response = self.session.put(f'{self.papi_url}/{url}', json=request_data, headers=headers)

        if response.status_code != status_codes.ok:
            error = response.json()
            raise BasePapiClientException(error)

        if response.text:
            return response.json()

        return response

    def _send_patch_request(self, url: str, request_data: Dict[str, Any], headers: Optional[Dict] = None):
        response = self.session.patch(f'{self.papi_url}/{url}', json=request_data, headers=headers)

        if response.status_code != status_codes.ok:
            error = response.json()
            raise BasePapiClientException(error)

        if response.text:
            return response.json()

        return response


class PapiClient(BasePapiClient):
    def __init__(
        self,
        papi_url: str,
        papi_auth_url: str,
        papi_client_id: str,
        papi_client_secret: str,
        solo_username: str = None,
        solo_password: str = None,
        headers: Optional[Dict] = None,
        proxies: Optional[Dict] = None,
    ):
        super().__init__(
            papi_url=papi_url,
            papi_auth_url=papi_auth_url,
            papi_client_id=papi_client_id,
            papi_client_secret=papi_client_secret,
            solo_username=solo_username,
            solo_password=solo_password,
            headers=headers,
            proxies=proxies,
        )

    def fetch_projects(
        self,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches projects
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url='projects', params={'offset': offset, 'limit': limit, 'filter': query}, headers=headers
        )

    def fetch_virtual_projects(
        self,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches virtual projects
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url='projects/virtual', params={'offset': offset, 'limit': limit, 'filter': query}, headers=headers
        )

    def fetch_project_raw_wells(
        self,
        project_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches project wells
        :param project_id:
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'projects/{project_id}/wells/raw',
            params={'offset': offset, 'limit': limit, 'filter': query},
            headers=headers,
        )

    def fetch_raw_well(
        self,
        well_id: str,
        headers: Optional[Dict] = None,
    ):
        return self._send_request(
            url=f'wells/{well_id}/raw',
            headers=headers,
        )

    def fetch_well_raw_trajectory(self, well_id: str, headers: Optional[Dict] = None):
        """
        Fetches well trajectory raw data
        :param well_id:
        :param headers:
        :return:
        """
        data = self._send_request(url=f'wells/{well_id}/trajectory/raw', headers=headers)

        return data['content']

    def fetch_well_raw_interpretations(
        self,
        well_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches well interpretations
        :param well_id:
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'wells/{well_id}/interpretations/raw',
            params={'offset': offset, 'limit': limit, 'filter': query},
            headers=headers,
        )

    def fetch_interpretation_horizons(
        self,
        interpretation_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches interpretation horizons
        :param interpretation_id:
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'interpretations/{interpretation_id}/horizons',
            params={'offset': offset, 'limit': limit, 'filter': query},
            headers=headers,
        )

    def fetch_interpretation_horizons_data(self, interpretation_id: str, md_step: int, headers: Optional[Dict] = None):
        """
        Fetches calculated by step horizons data
        :param interpretation_id:
        :param md_step:
        :param headers:
        :return:
        """
        data = self._send_request(
            url=f'interpretations/{interpretation_id}/horizons/data/spacing/{md_step}', headers=headers
        )

        return data['content']

    def fetch_interpretation_assembled_segments(self, interpretation_id: str, headers: Optional[Dict] = None):
        """
        Fetches interpretation assembled segments
        :param interpretation_id:
        :param headers:
        :return:
        """
        data = self._send_request(url=f'interpretations/{interpretation_id}/horizons/raw', headers=headers)

        return data['assembled_segments']

    def fetch_interpretation_starred_horizons(
        self, interpretation_id: str, headers: Optional[Dict] = None
    ) -> PapiStarredHorizons:
        """
        Fetches IDs of starred horizons
        :param interpretation_id:
        :param headers:
        :return:
        """
        starred_horizons = self._send_request(url=f'interpretations/{interpretation_id}/starred', headers=headers)

        return PapiStarredHorizons(
            top=starred_horizons.get('top'),
            center=starred_horizons.get('center'),
            bottom=starred_horizons.get('bottom'),
        )

    def fetch_interpretation_earth_models(
        self,
        interpretation_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches interpretation earth models
        :param interpretation_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'interpretations/{interpretation_id}/earthmodels',
            params={'offset': offset, 'limit': limit},
            headers=headers,
        )

    def fetch_earth_model_sections(
        self,
        earth_model_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches earth model sections
        :param earth_model_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        url = f'earthmodels/{earth_model_id}/data/raw'
        params = {'offset': offset, 'limit': limit}

        return self._send_request(url=url, params=params, headers=headers)['sections']

    def fetch_well_nested_wells(
        self,
        well_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches well nested wells
        :param well_id:
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'wells/{well_id}/nestedwells/raw',
            params={'offset': offset, 'limit': limit, 'filter': query},
            headers=headers,
        )

    def fetch_well_target_lines(
        self,
        well_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches well target lines data
        :param well_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'wells/{well_id}/targetlines/data',
            params={
                'offset': offset,
                'limit': limit,
            },
            headers=headers,
        )

    def create_well_nested_well(
        self,
        well_id: str,
        name: str,
        operator: str,
        api: str,
        xsrf: PapiVar,
        ysrf: PapiVar,
        kb: PapiVar,
        tie_in_tvd: PapiVar,
        tie_in_ns: PapiVar,
        tie_in_ew: PapiVar,
        headers: Optional[Dict] = None,
    ) -> PapiObjectCreationResult:
        url = f'wells/{well_id}/nestedwells'
        request_data = {
            'name': name,
            'operator': operator,
            'api': api,
            'xsrf': xsrf,
            'ysrf': ysrf,
            'kb': kb,
            'tie_in_tvd': tie_in_tvd,
            'tie_in_ns': tie_in_ns,
            'tie_in_ew': tie_in_ew,
        }

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def replace_nested_well_trajectory(
        self,
        nested_well_id: str,
        md_uom: str,
        incl_uom: str,
        azi_uom: str,
        trajectory_stations: PapiTrajectory,
        headers: Optional[Dict] = None,
    ):
        url = f'nestedwells/{nested_well_id}/trajectory'
        request_data = {
            'md_uom': md_uom,
            'incl_uom': incl_uom,
            'azi_uom': azi_uom,
            'trajectory_stations': trajectory_stations,
        }

        return self._send_put_request(url=url, request_data=request_data, headers=headers)

    def fetch_nested_well_raw_trajectory(self, nested_well_id: str, headers: dict = None):
        """
        Fetches nested well raw trajectory
        :param nested_well_id:
        :param headers:
        :return:
        """
        data = self._send_request(url=f'nestedwells/{nested_well_id}/trajectory/raw', headers=headers)

        return data['content']

    def fetch_well_logs(
        self,
        well_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches well logs
        :param well_id:
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'wells/{well_id}/logs',
            params={'offset': offset, 'limit': limit, 'filter': query},
            headers=headers,
        )

    def fetch_typewell_logs(
        self,
        typewell_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches typewell logs
        :param typewell_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'typewells/{typewell_id}/logs',
            params={
                'offset': offset,
                'limit': limit,
            },
            headers=headers,
        )

    def fetch_log_points(self, log_id: str, headers: Optional[Dict] = None):
        """
        Fetches log points data
        :param log_id:
        :param headers:
        :return:
        """
        data = self._send_request(url=f'logs/{log_id}/data/raw', headers=headers)

        return data['log_points']

    def fetch_well_mudlogs(
        self,
        well_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches well mudlogs
        :param well_id:
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'wells/{well_id}/mudlogs',
            params={'offset': offset, 'limit': limit, 'filter': query},
            headers=headers,
        )

    def fetch_typewell_mudlogs(
        self,
        typewell_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches typewell mudlogs
        :param typewell_id:
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'typewells/{typewell_id}/mudlogs',
            params={'offset': offset, 'limit': limit, 'filter': query},
            headers=headers,
        )

    def fetch_mudlog_logs(self, mudlog_id: str, headers: Optional[Dict] = None):
        """
        Fetches mudlog logs data
        :param mudlog_id:
        :param headers:
        :return:
        """
        data = self._send_request(url=f'mudlogs/{mudlog_id}/data/raw', headers=headers)

        return data['logs']

    def fetch_project_typewells(
        self,
        project_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: str = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches project typewells
        :param project_id:
        :param offset:
        :param limit:
        :param query:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'projects/{project_id}/typewells/raw',
            params={
                'offset': offset,
                'limit': limit,
                'filter': query,
            },
            headers=headers,
        )

    def fetch_typewell_raw_trajectory(self, typewell_id: str, headers: Optional[Dict] = None):
        """
        Fetches typewell trajectory raw data
        :param typewell_id:
        :param headers:
        :return:
        """
        data = self._send_request(url=f'typewells/{typewell_id}/trajectory/raw', headers=headers)

        return data['content']

    def create_well_topset(self, well_id: str, name: str, headers: Optional[Dict] = None) -> PapiObjectCreationResult:
        """
        Create topset in the well
        :param well_id:
        :param name:
        :param headers:
        :return:
        """
        url = f'wells/{well_id}/topsets'
        request_data = {'name': name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def create_typewell_topset(
        self, typewell_id: str, name: str, headers: Optional[Dict] = None
    ) -> PapiObjectCreationResult:
        """
        Create topset in the typewell
        :param typewell_id:
        :param name:
        :param headers:
        :return:
        """
        url = f'typewells/{typewell_id}/topsets'
        request_data = {'name': name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def create_nested_well_topset(
        self, nested_well_id: str, name: str, headers: Optional[Dict] = None
    ) -> PapiObjectCreationResult:
        """
        Create topset in the nestedwells
        :param nested_well_id:
        :param name:
        :param headers:
        :return:
        """
        url = f'nestedwells/{nested_well_id}/topsets'
        request_data = {'name': name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def fetch_well_topsets(
        self,
        well_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches well topsets
        :param well_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'wells/{well_id}/topsets',
            params={
                'offset': offset,
                'limit': limit,
            },
            headers=headers,
        )

    def fetch_typewell_topsets(
        self,
        typewell_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches typewell topsets
        :param typewell_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'typewells/{typewell_id}/topsets',
            params={
                'offset': offset,
                'limit': limit,
            },
            headers=headers,
        )

    def fetch_nested_well_topsets(
        self,
        nested_well_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches nested well topsets
        :param nested_well_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'nestedwells/{nested_well_id}/topsets',
            params={
                'offset': offset,
                'limit': limit,
            },
            headers=headers,
        )

    def create_well_target_line(
        self,
        well_id: str,
        name: str,
        origin_x: PapiVar,
        origin_y: PapiVar,
        origin_z: PapiVar,
        target_x: PapiVar,
        target_y: PapiVar,
        target_z: PapiVar,
        headers: Optional[Dict] = None,
    ) -> PapiObjectCreationResult:
        url = f'wells/{well_id}/targetlines'
        request_data = {
            'name': name,
            'origin_x': origin_x,
            'origin_y': origin_y,
            'origin_z': origin_z,
            'target_x': target_x,
            'target_y': target_y,
            'target_z': target_z,
        }

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def create_topset_top(
        self, topset_id: str, name: str, md: PapiVar, headers: Optional[Dict] = None
    ) -> PapiObjectCreationResult:
        """
        Create top in the topset
        :param topset_id:
        :param name:
        :param md:
        :param headers:
        :return:
        """
        url = f'topsets/{topset_id}/tops'
        request_data = {'name': name, 'md': md}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def fetch_topset_tops(
        self,
        topset_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches topset tops
        :param topset_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'topsets/{topset_id}/tops',
            params={
                'offset': offset,
                'limit': limit,
            },
            headers=headers,
        )

    def fetch_topset_starred_tops(self, topset_id: str, headers: Dict = None) -> PapiStarredTops:
        """
        Fetches IDs of starred tops
        :param topset_id:
        :param headers:
        :return:
        """
        starred_tops = self._send_request(url=f'topsets/{topset_id}/starred', headers=headers)

        return PapiStarredTops(
            top=starred_tops.get('top'), center=starred_tops.get('center'), bottom=starred_tops.get('bottom')
        )

    def create_well_log(self, well_id: str, name: str, headers: Optional[Dict] = None) -> PapiObjectCreationResult:
        """
        Create log in the well
        :param well_id:
        :param name:
        :param headers:
        :return:
        """
        url = f'wells/{well_id}/logs'
        request_data = {'name': name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def replace_log(
        self,
        log_id: str,
        log_points: List[PapiLogPoint],
        index_unit: Optional[str] = None,
        value_unit: Optional[str] = None,
        headers: Optional[Dict] = None,
    ):
        """
        Replace log data
        :param log_id:
        :param index_unit:
        :param log_points:
        :param value_unit:
        :param headers:
        :return:
        """
        url = f'logs/{log_id}/data'
        request_data = {
            'index_unit': index_unit,
            'value_unit': value_unit,
            'log_points': log_points,
        }

        return self._send_put_request(url=url, request_data=request_data, headers=headers)

    def update_log_meta(
        self, log_id: str, name: Optional[str] = None, unit: Optional[str] = None, headers: Optional[Dict] = None
    ) -> bool:
        """
        Update log meta
        :param log_id:
        :param name:
        :param unit:
        :param headers:
        :return:
        """
        url = f'logs/{log_id}'
        request_data = {'name': name, 'unit': unit}
        response = self._send_patch_request(url=url, request_data=request_data, headers=headers)

        return response.status_code == status_codes.ok

    def create_typewell_log(
        self, typewell_id: str, name: str, headers: Optional[Dict] = None
    ) -> PapiObjectCreationResult:
        """
        Create log in the typewell
        :param typewell_id:
        :param name:
        :param headers:
        :return:
        """
        url = f'typewells/{typewell_id}/logs'
        request_data = {'name': name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def fetch_traces(self, headers: Optional[Dict] = None):
        """
        Fetches traces collection
        :param headers:
        :return:
        """
        data = self._send_request(
            url='traces',
            headers=headers,
        )

        return data['content']

    def fetch_well_mapped_traces(self, well_id: str, trace_type: TraceType, headers: Optional[Dict] = None):
        """
        Fetches well traces with trace_type
        :param well_id:
        :param trace_type:
        :param headers:
        :return:
        """
        data = self._send_request(
            url=f'wells/{well_id}/traces/mapped/',
            params={'type': trace_type},
            headers=headers,
        )

        return data['content']

    def fetch_well_mapped_time_traces(self, well_id: str, headers: Optional[Dict] = None):
        return self.fetch_well_mapped_traces(well_id=well_id, trace_type='TIME', headers=headers)

    def fetch_well_mapped_calc_traces(self, well_id: str, headers: Optional[Dict] = None):
        return self.fetch_well_mapped_traces(well_id=well_id, trace_type='CALC', headers=headers)

    def fetch_well_time_trace(
        self,
        well_id: str,
        trace_id: str,
        time_from: Optional[str] = None,
        time_to: Optional[str] = None,
        trace_hash: Optional[str] = None,
        limit: Optional[int] = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches well time trace
        :param well_id:
        :param trace_id:
        :param time_from:
        :param time_to:
        :param trace_hash:
        :param limit:
        :param headers:
        :return:
        """
        data = self._send_request(
            url=f'wells/{well_id}/traces/{trace_id}/data/time/',
            params={'from': time_from, 'to': time_to, 'hash': trace_hash, 'limit': limit},
            headers=headers,
        )

        return data['content']

    def fetch_well_calc_trace(
        self,
        well_id: str,
        trace_id: str,
        time_from: Optional[str] = None,
        time_to: Optional[str] = None,
        trace_hash: Optional[str] = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches well calculated trace
        :param well_id:
        :param trace_id:
        :param trace_hash:
        :param time_from:
        :param time_to:
        :param headers:
        :return:
        """
        data = self._send_request(
            url=f'wells/{well_id}/traces/{trace_id}/data/calculated/',
            params={'from': time_from, 'to': time_to, 'hash': trace_hash},
            headers=headers,
        )

        return data['content']

    def update_well_meta(
        self,
        well_id: str,
        name: Optional[str] = None,
        operator: Optional[str] = None,
        api: Optional[str] = None,
        xsrf: Optional[PapiVar] = None,
        ysrf: Optional[PapiVar] = None,
        kb: Optional[PapiVar] = None,
        azimuth: Optional[PapiVar] = None,
        convergence: Optional[PapiVar] = None,
        tie_in_tvd: Optional[PapiVar] = None,
        tie_in_ns: Optional[PapiVar] = None,
        tie_in_ew: Optional[PapiVar] = None,
        headers: Optional[Dict] = None,
    ):
        return self._update_meta(
            url=f'wells/{well_id}/raw',
            name=name,
            operator=operator,
            api=api,
            xsrf=xsrf,
            ysrf=ysrf,
            kb=kb,
            azimuth=azimuth,
            convergence=convergence,
            tie_in_tvd=tie_in_tvd,
            tie_in_ns=tie_in_ns,
            tie_in_ew=tie_in_ew,
            headers=headers,
        )

    def update_typewell_meta(
        self,
        well_id: str,
        name: Optional[str] = None,
        operator: Optional[str] = None,
        api: Optional[str] = None,
        xsrf: Optional[PapiVar] = None,
        ysrf: Optional[PapiVar] = None,
        kb: Optional[PapiVar] = None,
        convergence: Optional[PapiVar] = None,
        tie_in_tvd: Optional[PapiVar] = None,
        tie_in_ns: Optional[PapiVar] = None,
        tie_in_ew: Optional[PapiVar] = None,
        headers: Optional[Dict] = None,
    ):
        return self._update_meta(
            url=f'typewells/{well_id}',
            name=name,
            operator=operator,
            api=api,
            xsrf=xsrf,
            ysrf=ysrf,
            kb=kb,
            convergence=convergence,
            tie_in_tvd=tie_in_tvd,
            tie_in_ns=tie_in_ns,
            tie_in_ew=tie_in_ew,
            headers=headers,
        )

    def update_nested_well_meta(
        self,
        well_id: str,
        name: Optional[str] = None,
        operator: Optional[str] = None,
        api: Optional[str] = None,
        xsrf: Optional[PapiVar] = None,
        ysrf: Optional[PapiVar] = None,
        kb: Optional[PapiVar] = None,
        tie_in_tvd: Optional[PapiVar] = None,
        tie_in_ns: Optional[PapiVar] = None,
        tie_in_ew: Optional[PapiVar] = None,
        headers: Optional[Dict] = None,
    ):
        return self._update_meta(
            url=f'nestedwells/{well_id}',
            name=name,
            operator=operator,
            api=api,
            xsrf=xsrf,
            ysrf=ysrf,
            kb=kb,
            tie_in_tvd=tie_in_tvd,
            tie_in_ns=tie_in_ns,
            tie_in_ew=tie_in_ew,
            headers=headers,
        )

    def _update_meta(
        self,
        url: str,
        name: Optional[str] = None,
        operator: Optional[str] = None,
        api: Optional[str] = None,
        xsrf: Optional[PapiVar] = None,
        ysrf: Optional[PapiVar] = None,
        kb: Optional[PapiVar] = None,
        azimuth: Optional[PapiVar] = None,
        convergence: Optional[PapiVar] = None,
        tie_in_tvd: Optional[PapiVar] = None,
        tie_in_ns: Optional[PapiVar] = None,
        tie_in_ew: Optional[PapiVar] = None,
        headers: Optional[Dict] = None,
    ):
        request_data = {
            'name': name,
            'operator': operator,
            'api': api,
            'xsrf': xsrf,
            'ysrf': ysrf,
            'kb': kb,
            'azimuth': azimuth,
            'convergence': convergence,
            'tie_in_tvd': tie_in_tvd,
            'tie_in_ns': tie_in_ns,
            'tie_in_ew': tie_in_ew,
        }

        response = self._send_patch_request(url=url, request_data=request_data, headers=headers)

        return response.status_code == status_codes.ok

    def create_well(
        self,
        project_id: str,
        name: str,
        operator: str,
        api: str,
        convergence: PapiVar,
        azimuth: PapiVar,
        kb: PapiVar,
        tie_in_tvd: PapiVar,
        tie_in_ns: PapiVar,
        tie_in_ew: PapiVar,
        xsrf_real: PapiVar,
        ysrf_real: PapiVar,
        headers: Optional[Dict] = None,
    ) -> PapiObjectCreationResult:
        """
        Create lateral in the project
        :param project_id:
        :param name:
        :param operator:
        :param api:
        :param convergence:
        :param azimuth:
        :param kb:
        :param tie_in_tvd:
        :param tie_in_ns:
        :param tie_in_ew:
        :param xsrf_real:
        :param ysrf_real:
        :param headers:
        :return:
        """
        url = f'projects/{project_id}/wells'
        request_data = {
            'name': name,
            'operator': operator,
            'api': api,
            'convergence': convergence,
            'azimuth': azimuth,
            'kb': kb,
            'tieintvd': tie_in_tvd,
            'tieinns': tie_in_ns,
            'tieinew': tie_in_ew,
            'xsrfreal': xsrf_real,
            'ysrfreal': ysrf_real,
        }

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def create_typewell(
        self,
        project_id: str,
        name: str,
        operator: str,
        api: str,
        convergence: PapiVar,
        kb: PapiVar,
        tie_in_tvd: PapiVar,
        tie_in_ns: PapiVar,
        tie_in_ew: PapiVar,
        xsrf_real: PapiVar,
        ysrf_real: PapiVar,
        headers: Optional[Dict] = None,
    ) -> PapiObjectCreationResult:
        """
        Create typewell in the project
        :param project_id:
        :param name:
        :param operator:
        :param api:
        :param convergence:
        :param kb:
        :param tie_in_tvd:
        :param tie_in_ns:
        :param tie_in_ew:
        :param xsrf_real:
        :param ysrf_real:
        :param headers:
        :return:
        """
        url = f'projects/{project_id}/typewells'
        request_data = {
            'name': name,
            'operator': operator,
            'api': api,
            'convergence': convergence,
            'kb': kb,
            'tieintvd': tie_in_tvd,
            'tieinns': tie_in_ns,
            'tieinew': tie_in_ew,
            'xsrfreal': xsrf_real,
            'ysrfreal': ysrf_real,
        }

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def fetch_well_linked_typewells(
        self,
        well_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        Fetches well linked typewells
        :param well_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'wells/{well_id}/linked',
            params={
                'offset': offset,
                'limit': limit,
            },
            headers=headers,
        )

    def fetch_well_comments(
        self,
        well_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        headers: Optional[Dict] = None,
    ):
        """
        :param well_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'wells/{well_id}/comments',
            params={
                'offset': offset,
                'limit': limit,
            },
            headers=headers,
        )

    def fetch_well_attributes(self, well_id: str, headers: Optional[Dict] = None):
        """
        :param well_id:
        :param headers:
        :return:
        """
        return self._send_request(
            url=f'wells/{well_id}/attributevalues',
            headers=headers,
        )

    def replace_well_trajectory(
        self,
        well_id: str,
        md_uom: str,
        incl_uom: str,
        azi_uom: str,
        trajectory_stations: PapiTrajectory,
        headers: Optional[Dict] = None,
    ):
        url = f'wells/{well_id}/trajectory'
        request_data = {
            'md_uom': md_uom,
            'incl_uom': incl_uom,
            'azi_uom': azi_uom,
            'trajectory_stations': trajectory_stations,
        }

        return self._send_put_request(url=url, request_data=request_data, headers=headers)

    def update_top_meta(self, top_id: str, name: str, md: PapiVar, headers: Optional[Dict] = None) -> bool:
        url = f'tops/{top_id}'
        request_data = {'name': name, 'md': md}
        response = self._send_patch_request(url=url, request_data=request_data, headers=headers)

        return response.status_code == status_codes.ok
