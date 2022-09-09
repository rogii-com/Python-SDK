from typing import Any, Dict, Optional

from oauthlib.oauth2 import BackendApplicationClient, LegacyApplicationClient
from requests import codes as status_codes
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from rogii_solo.papi.exceptions import AccessTokenFailureException, BasePapiClientException
from rogii_solo.papi.types import PapiStarredHorizons, PapiTrajectory, PapiVar


class BasePapiClient:
    DEFAULT_OFFSET = 0
    DEFAULT_LIMIT = 100
    LIMIT_MAX = 200
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self,
                 papi_url: str,
                 papi_auth_url: str,
                 papi_client_id: str,
                 papi_client_secret: str,
                 solo_username: str = None,
                 solo_password: str = None,
                 headers: Optional[Dict[str, Any]] = None,
                 proxies: Optional[Dict[str, Any]] = None
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
            'headers': self.headers
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
            client=client,
            token=token_data,
            auto_refresh_url=self.token_url,
            token_updater=self._update_token_data
        )

        # "Client credentials" grant type does not support token refreshing
        if isinstance(session._client, BackendApplicationClient):
            session.refresh_token = lambda *args, **kwargs: session.fetch_token(**token_params)

        session.headers.update({
            'Authorization': f"Bearer {token_data['access_token']}"
        })
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
        self.session.headers.update({
            'Authorization': f"Bearer {token_data['access_token']}"
        })

    def _send_request(self,
                      url: str,
                      params: Optional[Dict[str, Any]] = None,
                      headers: Optional[Dict[str, Any]] = None
                      ):
        response = self.session.get(f"{self.papi_url}/{url}", params=params, headers=headers)

        if response.status_code != status_codes.ok:
            error = response.json()
            raise BasePapiClientException(error)

        if response.text:
            return response.json()

    def _send_post_request(self,
                           url: str,
                           request_data: Dict[str, Any],
                           headers: Optional[Dict[str, Any]] = None
                           ):
        response = self.session.post(f"{self.papi_url}/{url}", json=request_data, headers=headers)

        if response.status_code != status_codes.ok:
            error = response.json()
            raise BasePapiClientException(error)

        if response.text:
            return response.json()

    def _send_put_request(self,
                          url: str,
                          request_data: Dict[str, Any],
                          headers: Optional[Dict[str, Any]] = None
                          ):
        response = self.session.put(f"{self.papi_url}/{url}", json=request_data, headers=headers)

        if response.status_code != status_codes.ok:
            error = response.json()
            raise BasePapiClientException(error)

        if response.text:
            return response.json()


class PapiClient(BasePapiClient):
    def __init__(self,
                 papi_url: str,
                 papi_auth_url: str,
                 papi_client_id: str,
                 papi_client_secret: str,
                 solo_username: str = None,
                 solo_password: str = None,
                 headers: Optional[Dict[str, Any]] = None,
                 proxies: Optional[Dict[str, Any]] = None
                 ):
        super().__init__(
            papi_url=papi_url,
            papi_auth_url=papi_auth_url,
            papi_client_id=papi_client_id,
            papi_client_secret=papi_client_secret,
            solo_username=solo_username,
            solo_password=solo_password,
            headers=headers,
            proxies=proxies
        )

    def fetch_projects(self,
                       offset: int = BasePapiClient.DEFAULT_OFFSET,
                       limit: int = BasePapiClient.DEFAULT_LIMIT,
                       project_filter: str = None,
                       headers: Optional[Dict[str, Any]] = None
                       ):
        """
        Fetches projects
        :param offset:
        :param limit:
        :param project_filter:
        :param headers:
        :return:
        """

        return self._send_request(
            url='projects',
            params={
                'offset': offset,
                'limit': limit,
                'filter': project_filter
            },
            headers=headers
        )

    def fetch_virtual_projects(self,
                               offset: int = BasePapiClient.DEFAULT_OFFSET,
                               limit: int = BasePapiClient.DEFAULT_LIMIT,
                               project_filter: str = None,
                               headers: Optional[Dict[str, Any]] = None
                               ):
        """
        Fetches virtual projects
        :param offset:
        :param limit:
        :param project_filter:
        :param headers:
        :return:
        """

        return self._send_request(
            url='projects/virtual',
            params={
                'offset': offset,
                'limit': limit,
                'filter': project_filter
            },
            headers=headers
        )

    def fetch_project_wells(self,
                            project_id: str,
                            offset: int = BasePapiClient.DEFAULT_OFFSET,
                            limit: int = BasePapiClient.DEFAULT_LIMIT,
                            well_filter: str = None,
                            headers: Optional[Dict[str, Any]] = None
                            ):
        """
        Fetches project wells
        :param project_id:
        :param offset:
        :param limit:
        :param well_filter:
        :param headers:
        :return:
        """

        return self._send_request(
            url=f'projects/{project_id}/wells/raw',
            params={
                'offset': offset,
                'limit': limit,
                'filter': well_filter
            },
            headers=headers
        )

    def fetch_well_raw_trajectory(self, well_id: str, headers: Optional[Dict[str, Any]] = None):
        """
        Fetches well trajectory raw data
        :param well_id:
        :param headers:
        :return:
        """

        data = self._send_request(url=f'wells/{well_id}/trajectory/raw', headers=headers)

        return data['content']

    def fetch_well_raw_interpretations(self,
                                       well_id: str,
                                       offset: int = BasePapiClient.DEFAULT_OFFSET,
                                       limit: int = BasePapiClient.DEFAULT_LIMIT,
                                       interpretation_filter: str = None,
                                       headers: Optional[Dict[str, Any]] = None
                                       ):
        """
        Fetches well interpretations
        :param well_id:
        :param offset:
        :param limit:
        :param interpretation_filter:
        :param headers:
        :return:
        """

        return self._send_request(
            url=f'wells/{well_id}/interpretations/raw',
            params={
                'offset': offset,
                'limit': limit,
                'filter': interpretation_filter
            },
            headers=headers
        )

    def fetch_interpretation_horizons(self,
                                      interpretation_id: str,
                                      offset: int = BasePapiClient.DEFAULT_OFFSET,
                                      limit: int = BasePapiClient.DEFAULT_LIMIT,
                                      horizon_filter: str = None,
                                      headers: Optional[Dict[str, Any]] = None
                                      ):
        """
        Fetches interpretation horizons
        :param interpretation_id:
        :param offset:
        :param limit:
        :param horizon_filter:
        :param headers:
        :return:
        """

        return self._send_request(
            url=f'interpretations/{interpretation_id}/horizons',
            params={
                'offset': offset,
                'limit': limit,
                'filter': horizon_filter
            },
            headers=headers
        )

    def fetch_interpretation_assembled_segments(self,
                                                interpretation_id: str,
                                                headers: Optional[Dict[str, Any]] = None
                                                ):
        """
        Fetches interpretation assembled segments
        :param interpretation_id:
        :param headers:
        :return:
        """

        data = self._send_request(url=f'interpretations/{interpretation_id}/horizons/raw', headers=headers)

        return data['assembled_segments']

    def fetch_interpretation_starred_horizons(self,
                                              interpretation_id: str,
                                              headers: Optional[Dict[str, Any]] = None
                                              ) -> PapiStarredHorizons:
        """
        Fetches IDs of starred horizons
        :param interpretation_id:
        :param headers:
        :return:
        """
        starred_horizons: PapiStarredHorizons = self._send_request(
            url=f'interpretations/{interpretation_id}/starred', headers=headers
        )

        return PapiStarredHorizons(
            top=starred_horizons['top'],
            center=starred_horizons['center'],
            bottom=starred_horizons['bottom']
        )

    def fetch_well_nested_wells(self,
                                well_id: str,
                                offset: int = BasePapiClient.DEFAULT_OFFSET,
                                limit: int = BasePapiClient.DEFAULT_LIMIT,
                                headers: Optional[Dict[str, Any]] = None
                                ):
        """
        Fetches well nested wells
        :param well_id:
        :param offset:
        :param limit:
        :param headers:
        :return:
        """

        return self._send_request(
            url=f'wells/{well_id}/nestedwells/raw',
            params={
                'offset': offset,
                'limit': limit
            },
            headers=headers
        )

    def fetch_well_target_lines(self,
                                well_id: str,
                                offset: int = BasePapiClient.DEFAULT_OFFSET,
                                limit: int = BasePapiClient.DEFAULT_LIMIT,
                                headers: Optional[Dict[str, Any]] = None
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
            headers=headers
        )

    def create_well_nested_well(self,
                                well_id: str,
                                nested_well_name: str,
                                operator: str,
                                api: str,
                                xsrf: PapiVar,
                                ysrf: PapiVar,
                                kb: PapiVar,
                                tie_in_tvd: PapiVar,
                                tie_in_ns: PapiVar,
                                tie_in_ew: PapiVar,
                                headers: Optional[Dict[str, Any]] = None
                                ):
        url = f'wells/{well_id}/nestedwells'
        request_data = {
            'name': nested_well_name,
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

    def replace_nested_well_trajectory(self,
                                       nested_well_id: str,
                                       md_uom: str,
                                       incl_uom: str,
                                       azi_uom: str,
                                       trajectory_stations: PapiTrajectory,
                                       headers: Optional[Dict[str, Any]] = None
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

    def fetch_project_typewells(self,
                                project_id: str,
                                offset: int = BasePapiClient.DEFAULT_OFFSET,
                                limit: int = BasePapiClient.DEFAULT_LIMIT,
                                typewell_filter: str = None,
                                headers: Optional[Dict[str, Any]] = None
                                ):
        """
        Fetches project typewells
        :param project_id:
        :param offset:
        :param limit:
        :param typewell_filter:
        :param headers:
        :return:
        """

        return self._send_request(
            url=f'projects/{project_id}/typewells',
            params={
                'offset': offset,
                'limit': limit,
                'filter': typewell_filter,
            },
            headers=headers
        )

    def fetch_typewell_raw_trajectory(self, typewell_id: str, headers: Optional[Dict[str, Any]] = None):
        """
        Fetches typewell trajectory raw data
        :param typewell_id:
        :param headers:
        :return:
        """

        data = self._send_request(url=f'typewells/{typewell_id}/trajectory/raw', headers=headers)

        return data['content']

    def create_well_topset(self,
                           well_id: str,
                           topset_name: str,
                           headers: Optional[Dict[str, Any]] = None
                           ):
        """
        Create topset in the well
        :param well_id:
        :param topset_name:
        :param headers:
        :return:
        """

        url = f'wells/{well_id}/topsets'
        request_data = {'name': topset_name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def create_typewell_topset(self,
                               typewell_id: str,
                               topset_name: str,
                               headers: Optional[Dict[str, Any]] = None
                               ):
        """
        Create topset in the typewell
        :param typewell_id:
        :param topset_name:
        :param headers:
        :return:
        """

        url = f'typewells/{typewell_id}/topsets'
        request_data = {'name': topset_name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def create_nested_well_topset(self,
                                  nested_well_id: str,
                                  topset_name: str,
                                  headers: Optional[Dict[str, Any]] = None
                                  ):
        """
        Create topset in the nestedwells
        :param nested_well_id:
        :param topset_name:
        :param headers:
        :return:
        """

        url = f'nestedwells/{nested_well_id}/topsets'
        request_data = {'name': topset_name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def fetch_well_topsets(self,
                           well_id: str,
                           offset: int = BasePapiClient.DEFAULT_OFFSET,
                           limit: int = BasePapiClient.DEFAULT_LIMIT,
                           headers: Optional[Dict[str, Any]] = None
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
            headers=headers
        )

    def fetch_typewell_topsets(self,
                               typewell_id: str,
                               offset: int = BasePapiClient.DEFAULT_OFFSET,
                               limit: int = BasePapiClient.DEFAULT_LIMIT,
                               headers: Optional[Dict[str, Any]] = None
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
            headers=headers
        )

    def fetch_nested_well_topsets(self,
                                  nested_well_id: str,
                                  offset: int = BasePapiClient.DEFAULT_OFFSET,
                                  limit: int = BasePapiClient.DEFAULT_LIMIT,
                                  headers: Optional[Dict[str, Any]] = None
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
            headers=headers
        )

    def create_well_target_line(self,
                                well_id: str,
                                target_line_name: str,
                                origin_x: PapiVar,
                                origin_y: PapiVar,
                                origin_z: PapiVar,
                                target_x: PapiVar,
                                target_y: PapiVar,
                                target_z: PapiVar,
                                headers: Optional[Dict[str, Any]] = None
                                ):
        url = f'wells/{well_id}/targetlines'
        request_data = {
            'name': target_line_name,
            'origin_x': origin_x,
            'origin_y': origin_y,
            'origin_z': origin_z,
            'target_x': target_x,
            'target_y': target_y,
            'target_z': target_z,
        }

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def create_topset_top(self,
                          topset_id: str,
                          top_name: str,
                          md: PapiVar,
                          headers: Optional[Dict[str, Any]] = None
                          ):
        """
        Create top in the topset
        :param topset_id:
        :param top_name:
        :param md:
        :param headers:
        :return:
        """

        url = f'topsets/{topset_id}/tops'
        request_data = {
            'name': top_name,
            'md': md,
        }

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def fetch_topset_tops(self,
                          topset_id: str,
                          offset: int = BasePapiClient.DEFAULT_OFFSET,
                          limit: int = BasePapiClient.DEFAULT_LIMIT,
                          headers: Optional[Dict[str, Any]] = None
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
            headers=headers
        )
