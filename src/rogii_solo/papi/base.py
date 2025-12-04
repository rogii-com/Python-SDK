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
    """
    :class:`BasePapiClient` is a base class for the PapiClient.

    :example:

        .. code-block:: python

            from rogii_solo.papi.base import BasePapiClient

            papi_client_id = ... # Input your client ID
            papi_client_secret = ... # Input your client secret
            papi_auth_url = ... # Input your papi auth url
            papi_url = ... # Input your papi url
            solo_username = ... # Input your solo username
            solo_password = ... # Input your solo password
            headers = ... # Input your headers or None
            proxies = ... # Input your proxy or None

            client = BasePapiClient(
                papi_client_id=papi_client_id,
                papi_client_secret=papi_client_secret,
                papi_auth_url=papi_auth_url,
                papi_url=papi_url,
                solo_username=solo_username,
                solo_password=solo_password,
                headers=headers,
                proxies=proxies
            )
    """

    DEFAULT_OFFSET = 0
    """Constant parameter equaled to 0"""

    DEFAULT_LIMIT = 100
    """Constant parameter equaled to 100"""

    LIMIT_MAX = 200
    """Constant parameter equaled to 200"""

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    """Constant parameter equaled to '%Y-%m-%dT%H:%M:%SZ'"""

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
        """PAPI url"""

        self.token_url = f'{papi_auth_url}/token'
        """Token url"""

        self.papi_client_id = papi_client_id
        """PAPI client id"""

        self.papi_client_secret = papi_client_secret
        """PAPI client secret"""

        self.solo_username = solo_username
        """Solo username"""

        self.solo_password = solo_password
        """Solo password"""

        self.headers = headers or {}
        """Headers"""

        self.proxies = proxies or {}
        """Proxies"""

        self._session = None

    @property
    def session(self):
        """
        Get the session object for the PAPI client.

        :return: The session object.

        :example:

        .. code-block:: python

            from rogii_solo.papi.base import BasePapiClient

            papi_client_id = ... # Input your client ID
            papi_client_secret = ... # Input your client secret
            papi_auth_url = ... # Input your papi auth url
            papi_url = ... # Input your papi url
            solo_username = ... # Input your solo username
            solo_password = ... # Input your solo password
            headers = ... # Input your headers or None
            proxies = ... # Input your proxy or None

            client = BasePapiClient(
                papi_client_id=papi_client_id,
                papi_client_secret=papi_client_secret,
                papi_auth_url=papi_auth_url,
                papi_url=papi_url,
                solo_username=solo_username,
                solo_password=solo_password,
                headers=headers,
                proxies=proxies
            )

            # Get Client's session
            session = client.session
            print(session)
        """
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
    """
    :class:`PapiClient` for interacting with the Solo Platform API (PAPI).
    Provides low-level access to PAPI endpoints for data fetching and editing.

    :example:

        .. code-block:: python

            from rogii_solo.papi.base import PapiClient

            papi_client_id = ... # Input your client ID
            papi_client_secret = ... # Input your client secret
            papi_auth_url = ... # Input your papi auth url
            papi_url = ... # Input your papi url
            solo_username = ... # Input your solo username
            solo_password = ... # Input your solo password
            headers = ... # Input your headers or None
            proxies = ... # Input your proxy or None

            client = PapiClient(
                papi_client_id=papi_client_id,
                papi_client_secret=papi_client_secret,
                papi_auth_url=papi_auth_url,
                papi_url=papi_url,
                solo_username=solo_username,
                solo_password=solo_password,
                headers=headers,
                proxies=proxies
            )

            # Fetch projects
            projects = client.fetch_projects()
            print(projects)
    """

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
        query: Optional[str] = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetch a list of projects from the PAPI service.

        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing project data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 projects
            projects = client.fetch_projects(offset=0, limit=100)

            # Fetch projects with a filter query
            filtered_projects = client.fetch_projects(query='Project1')
        """
        return self._send_request(
            url='projects', params={'offset': offset, 'limit': limit, 'filter': query}, headers=headers
        )

    def fetch_virtual_projects(
        self,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: Optional[str] = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetch a list of virtual projects from the PAPI service.

        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing virtual project data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 virtual projects
            virtual_projects = client.fetch_virtual_projects(offset=0, limit=100)

            # Fetch virtual projects with a filter query
            filtered_projects = client.fetch_virtual_projects(query='Project1')
        """
        return self._send_request(
            url='projects/virtual', params={'offset': offset, 'limit': limit, 'filter': query}, headers=headers
        )

    def fetch_project_raw_wells(
        self,
        project_id: str,
        offset: int = BasePapiClient.DEFAULT_OFFSET,
        limit: int = BasePapiClient.DEFAULT_LIMIT,
        query: Optional[str] = None,
        headers: Optional[Dict] = None,
    ):
        """
        Fetch a list of raw well data for a specific project.

        :param project_id: UUID of the project.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing well data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 wells for a project
            wells = client.fetch_project_raw_wells(
                project_id='ProjectID',
                offset=0,
                limit=100
            )

            # Fetch wells with a filter query
            filtered_wells = client.fetch_project_raw_wells(
                project_id='ProjectUUID',
                query='Well1'
            )
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
        """
        Fetch raw data for a specific well.

        :param well_id: UUID of the well.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing well data.

        :example:

        .. code-block:: python

            # Fetch data for a specific well
            well_data = client.fetch_raw_well(well_id='WellUUID')
        """
        return self._send_request(
            url=f'wells/{well_id}/raw',
            headers=headers,
        )

    def fetch_well_raw_trajectory(self, well_id: str, headers: Optional[Dict] = None):
        """
        Fetch raw trajectory data for a specific well.

        :param well_id: UUID of the well.
        :param headers: Optional additional HTTP headers.

        :return: List of trajectory points.

        :example:

        .. code-block:: python

            # Fetch trajectory data for a well
            trajectory = client.fetch_well_raw_trajectory(well_id='WellUUID')
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
        Fetch raw interpretation data for a specific well.

        :param well_id: UUID of the well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing interpretation data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 interpretations for a well
            interpretations = client.fetch_well_raw_interpretations(
                well_id='WellUUID',
                offset=0,
                limit=100
            )

            # Fetch interpretations with a filter query
            filtered_interpretations = client.fetch_well_raw_interpretations(
                well_id='WellUUID',
                query='Interpretation1'
            )
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
        Fetch horizons for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing horizon data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 horizons for an interpretation
            horizons = client.fetch_interpretation_horizons(
                interpretation_id="interpretation_uuid",
                offset=0,
                limit=100
            )

            # Fetch horizons with a filter query
            filtered_horizons = client.fetch_interpretation_horizons(
                interpretation_id='InterpretationUUID',
                query='Horizon1'
            )
        """
        return self._send_request(
            url=f'interpretations/{interpretation_id}/horizons',
            params={'offset': offset, 'limit': limit, 'filter': query},
            headers=headers,
        )

    def fetch_interpretation_horizons_data(self, interpretation_id: str, md_step: int, headers: Optional[Dict] = None):
        """
        Fetch horizon data points for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.
        :param md_step: Step size for measured depth sampling.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing horizon data points.

        :example:

        .. code-block:: python

            # Fetch horizon data with 1-meter step
            horizon_data = client.fetch_interpretation_horizons_data(
                interpretation_id='InterpretationUUID',
                md_step=1
            )
        """
        data = self._send_request(
            url=f'interpretations/{interpretation_id}/horizons/data/spacing/{md_step}', headers=headers
        )

        return data['content']

    def fetch_interpretation_assembled_segments(self, interpretation_id: str, headers: Optional[Dict] = None):
        """
        Fetch assembled segments for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing assembled segments data.

        :example:

        .. code-block:: python

            # Fetch assembled segments for an interpretation
            segments = client.fetch_interpretation_assembled_segments(
                interpretation_id='InterpretationUUID'
            )
        """
        data = self._send_request(url=f'interpretations/{interpretation_id}/horizons/raw', headers=headers)

        return data['assembled_segments']

    def fetch_interpretation_starred_horizons(
        self, interpretation_id: str, headers: Optional[Dict] = None
    ) -> PapiStarredHorizons:
        """
        Fetch IDs of starred horizons for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiStarredHorizons` containing starred horizon UUIDs.

        :example:

        .. code-block:: python

            # Fetch starred horizons for an interpretation
            starred = client.fetch_interpretation_starred_horizons(
                interpretation_id='InterpretationUUID'
            )
            print(f'Top horizon: {starred.top}')
            print(f'Center horizon: {starred.center}')
            print(f'Bottom horizon: {starred.bottom}')
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
        Fetch earth models for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param headers: Optional additional HTTP headers.
        :return: Dictionary containing earth model data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 earth models for an interpretation
            earth_models = client.fetch_interpretation_earth_models(
                interpretation_id='InterpretationUUID',
                offset=0,
                limit=100
            )
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
        Fetch sections for a specific earth model.

        :param earth_model_id: UUID of the earth model.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing section data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 sections for an earth model
            sections = client.fetch_earth_model_sections(
                earth_model_id='EarthModelUUID',
                offset=0,
                limit=100
            )
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
        Fetches well' well plans

        :param well_id: UUID of the well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing well plan data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 well plans
            well_plans = client.fetch_well_nested_wells(
                well_id='WellUUID',
                offset=0,
                limit=100,
                query='WellPlan1'
            )
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

        :param well_id: UUID of the well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing target line data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 well plans
            target_lines = client.fetch_well_target_lines(
                well_id='WellUUID',
                offset=0,
                limit=100,
            )
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
        """
        Create a new well plan within an existing well.

        :param well_id: UUID of the parent well.
        :param name: Name of the well plan.
        :param operator: Operator of the well plan.
        :param api: API number of the well plan.
        :param xsrf: Surface X coordinate as :class:`~rogii_solo.papi.types.PapiVar`.
        :param ysrf: Surface Y coordinate as :class:`~rogii_solo.papi.types.PapiVar`.
        :param kb: Kelly bushing elevation as :class:`~rogii_solo.papi.types.PapiVar`.
        :param tie_in_tvd: Tie-in true vertical depth as :class:`~rogii_solo.papi.types.PapiVar`.
        :param tie_in_ns: Tie-in North-South offset as :class:`~rogii_solo.papi.types.PapiVar`.
        :param tie_in_ew: Tie-in East-West offset as :class:`~rogii_solo.papi.types.PapiVar`.
        :param headers: Optional additional HTTP headers.

        :return: :class:`~rogii_solo.papi.types.PapiObjectCreationResult` containing the created object's ID.

        :example:

        .. code-block:: python

            # Create a new well plan
            result = client.create_well_nested_well(
                well_id='WellUUID',
                name='WellPlan1',
                operator='Operator',
                api='12345',
                xsrf={'val': 100.0},
                ysrf={'val': 200.0},
                kb={'val': 1000.0},
                tie_in_tvd={'val': 2000.0},
                tie_in_ns={'val': 50.0},
                tie_in_ew={'val': -30.0}
            )
            print(f'Created well plan with ID: {result.id}')
        """
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
        """
        Replace the trajectory of a well plan.

        :param nested_well_id: UUID of the well plan.
        :param md_uom: Unit of measure for measured depth.
        :param incl_uom: Unit of measure for inclination.
        :param azi_uom: Unit of measure for azimuth.
        :param trajectory_stations: List of trajectory points as :class:`~rogii_solo.papi.types.PapiTrajectory`.
        :param headers: Optional additional HTTP headers.
        :return: Response from the server.

        :example:

        .. code-block:: python

            # Replace well plan trajectory
            trajectory = [
                {'md': {'val': 0}, 'incl': {'val': 0}, 'azi': {'val': 0}},
                {'md': {'val': 100}, 'incl': {'val': 5}, 'azi': {'val': 180}},
            ]
            client.replace_nested_well_trajectory(
                nested_well_id='WellPlanUUID',
                md_uom='ft',
                incl_uom='deg',
                azi_uom='deg',
                trajectory_stations=trajectory
            )
        """
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
        Fetch raw trajectory data for a specific nested well.

        :param nested_well_id: UUID of the nested well.
        :param headers: Optional additional HTTP headers.

        :return: List of trajectory points.

        :example:

        .. code-block:: python

            # Fetch trajectory data for a well plan
            trajectory = client.fetch_nested_well_raw_trajectory(
                nested_well_id='WellPlanUUID'
            )
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
        Fetch logs for a specific well.

        :param well_id: UUID of the well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing log data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 logs for a well
            logs = client.fetch_well_logs(
                well_id='WellUUID',
                offset=0,
                limit=100
            )

            # Fetch logs with a filter query
            filtered_logs = client.fetch_well_logs(
                well_id='WellUUID',
                query='Log1'
            )
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
        Fetch logs for a specific type well.

        :param typewell_id: UUID of the type well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing log data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 logs for a type well
            logs = client.fetch_typewell_logs(
                typewell_id='TypeWellUUID',
                offset=0,
                limit=100
            )
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
        Fetch data points for a specific log.

        :param log_id: UUID of the log.
        :param headers: Optional additional HTTP headers.

        :return: List of log data points.

        :example:

        .. code-block:: python

            # Fetch data points for a log
            points = client.fetch_log_points(log_id='LogUUID')
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
        Fetch mudlogs for a specific well.

        :param well_id: UUID of the well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing mudlog data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 mudlogs for a well
            mudlogs = client.fetch_well_mudlogs(
                well_id='WellUUID',
                offset=0,
                limit=100
            )

            # Fetch mudlogs with a filter query
            filtered_mudlogs = client.fetch_well_mudlogs(
                well_id='WellUUID',
                query='Mudlog1'
            )
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
        Fetch mudlogs for a specific type well.

        :param typewell_id: UUID of the type well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing mudlog data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 mudlogs for a type well
            mudlogs = client.fetch_typewell_mudlogs(
                typewell_id='TypeWellUUID',
                offset=0,
                limit=100
            )

            # Fetch mudlogs with a filter query
            filtered_mudlogs = client.fetch_typewell_mudlogs(
                typewell_id='TypeWellUUID',
                query='Mudlog1'
            )
        """
        return self._send_request(
            url=f'typewells/{typewell_id}/mudlogs',
            params={'offset': offset, 'limit': limit, 'filter': query},
            headers=headers,
        )

    def fetch_mudlog_logs(self, mudlog_id: str, headers: Optional[Dict] = None):
        """
        Fetch log data for a specific mudlog.

        :param mudlog_id: UUID of the mudlog.
        :param headers: Optional additional HTTP headers.

        :return: List of log data points.

        :example:

        .. code-block:: python

            # Fetch log data for a mudlog
            log_data = client.fetch_mudlog_logs(mudlog_id='MudlogUUID')
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
        Fetch type wells for a specific project.

        :param project_id: UUID of the project.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param query: Optional filter query string.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing type well data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 type wells for a project
            typewells = client.fetch_project_typewells(
                project_id='ProjectUUID',
                offset=0,
                limit=100
            )

            # Fetch type wells with a filter query
            filtered_typewells = client.fetch_project_typewells(
                project_id='ProjectUUID',
                query='TypeWell1'
            )
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
        Fetch raw trajectory data for a specific type well.

        :param typewell_id: UUID of the type well.
        :param headers: Optional additional HTTP headers.

        :return: List of trajectory points.

        :example:

        .. code-block:: python

            # Fetch trajectory data for a type well
            trajectory = client.fetch_typewell_raw_trajectory(
                typewell_id='TypeWellUUID'
            )
        """
        data = self._send_request(url=f'typewells/{typewell_id}/trajectory/raw', headers=headers)

        return data['content']

    def create_well_topset(self, well_id: str, name: str, headers: Optional[Dict] = None) -> PapiObjectCreationResult:
        """
        Create a new topset in a well.

        :param well_id: UUID of the well.
        :param name: Name of the topset.
        :param headers: Optional additional HTTP headers.
        :return: :class:`PapiObjectCreationResult` containing the created object's ID.

        :example:

        .. code-block:: python

            # Create a new topset in a well
            result = client.create_well_topset(
                well_id='WellUUID',
                name='Topset1'
            )
            print(f'Created topset with ID: {result.id}')
        """
        url = f'wells/{well_id}/topsets'
        request_data = {'name': name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def create_typewell_topset(
        self, typewell_id: str, name: str, headers: Optional[Dict] = None
    ) -> PapiObjectCreationResult:
        """
        Create a new topset in a type well.

        :param typewell_id: UUID of the type well.
        :param name: Name of the topset.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiObjectCreationResult` containing the created object's ID.

        :example:

        .. code-block:: python

            # Create a new topset in a type well
            result = client.create_typewell_topset(
                typewell_id='TypeWellUUID',
                name='Topset1'
            )
            print(f'Created topset with ID: {result.id}')
        """
        url = f'typewells/{typewell_id}/topsets'
        request_data = {'name': name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def create_nested_well_topset(
        self, nested_well_id: str, name: str, headers: Optional[Dict] = None
    ) -> PapiObjectCreationResult:
        """
        Create a new topset in a nested well.

        :param nested_well_id: UUID of the nested well.
        :param name: Name of the topset.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiObjectCreationResult` containing the created object's ID.

        :example:

        .. code-block:: python

            # Create a new topset in a nested well
            result = client.create_nested_well_topset(
                nested_well_id='NestedWellUUID',
                name='Topset1'
            )
            print(f'Created topset with ID: {result.id}')
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
        Fetch topsets for a specific well.

        :param well_id: UUID of the well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing topset data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 topsets for a well
            topsets = client.fetch_well_topsets(
                well_id='WellUUID',
                offset=0,
                limit=100
            )
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
        Fetch topsets for a specific type well.

        :param typewell_id: UUID of the type well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing topset data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 topsets for a type well
            topsets = client.fetch_typewell_topsets(
                typewell_id='TypeWellUUID',
                offset=0,
                limit=100
            )
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
        Fetch topsets for a specific nested well.

        :param nested_well_id: UUID of the nested well.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing topset data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 topsets for a nested well
            topsets = client.fetch_nested_well_topsets(
                nested_well_id='NestedWellUUID',
                offset=0,
                limit=100
            )
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
        """
        Create a new target line in a well.

        :param well_id: UUID of the well.
        :param name: Name of the target line.
        :param origin_x: X coordinate of the origin point as :class:`PapiVar`.
        :param origin_y: Y coordinate of the origin point as :class:`PapiVar`.
        :param origin_z: Z coordinate of the origin point as :class:`PapiVar`.
        :param target_x: X coordinate of the target point as :class:`PapiVar`.
        :param target_y: Y coordinate of the target point as :class:`PapiVar`.
        :param target_z: Z coordinate of the target point as :class:`PapiVar`.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiObjectCreationResult` containing the created object's ID.

        :example:

        .. code-block:: python

            # Create a new target line
            result = client.create_well_target_line(
                well_id='WellUUID',
                name='TargetLine1',
                origin_x={'val': 100.0},
                origin_y={'val': 200.0},
                origin_z={'val': 300.0},
                target_x={'val': 400.0},
                target_y={'val': 500.0},
                target_z={'val': 600.0}
            )
            print(f'Created target line with ID: {result.id}')
        """
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
        Create a new top in a topset.

        :param topset_id: UUID of the topset.
        :param name: Name of the top.
        :param md: Measured depth of the top as :class:`PapiVar`.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiObjectCreationResult` containing the created object's ID.

        :example:

        .. code-block:: python

            # Create a new top in a topset
            result = client.create_topset_top(
                topset_id='TopsetUUID',
                name='Top1',
                md={'val': 1000.0}
            )
            print(f'Created top with ID: {result.id}')
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
        Fetch tops for a specific topset.

        :param topset_id: UUID of the topset.
        :param offset: Number of items to skip before starting to collect the result set.
        :param limit: Maximum number of items to return.
        :param headers: Optional additional HTTP headers.

        :return: Dictionary containing top data and pagination information.

        :example:

        .. code-block:: python

            # Fetch first 100 tops for a topset
            tops = client.fetch_topset_tops(
                topset_id='TopsetUUID',
                offset=0,
                limit=100
            )
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
        Fetch IDs of starred tops for a specific topset.

        :param topset_id: UUID of the topset.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiStarredTops` containing starred top UUIDs.

        :example:

        .. code-block:: python

            # Fetch starred tops for a topset
            starred = client.fetch_topset_starred_tops(
                topset_id='TopsetUUID'
            )
            print(f'Top: {starred.top}')
            print(f'Center: {starred.center}')
            print(f'Bottom: {starred.bottom}')
        """
        starred_tops = self._send_request(url=f'topsets/{topset_id}/starred', headers=headers)

        return PapiStarredTops(
            top=starred_tops.get('top'), center=starred_tops.get('center'), bottom=starred_tops.get('bottom')
        )

    def create_well_log(self, well_id: str, name: str, headers: Optional[Dict] = None) -> PapiObjectCreationResult:
        """
        Create a new log in a well.

        :param well_id: UUID of the well.
        :param name: Name of the log.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiObjectCreationResult` containing the created object's ID.

        :example:

        .. code-block:: python

            # Create a new log in a well
            result = client.create_well_log(
                well_id='WellUUID',
                name='Log1'
            )
            print(f'Created log with ID: {result.id}')
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
        Replace data points in a log.

        :param log_id: UUID of the log.
        :param log_points: List of log points as :class:`PapiLogPoint`.
        :param index_unit: Optional unit of measure for the index values.
        :param value_unit: Optional unit of measure for the data values.
        :param headers: Optional additional HTTP headers.

        :return: Response from the server.

        :example:

        .. code-block:: python

            # Replace log data points
            points = [
                {'index': {'val': 0}, 'value': {'val': 100}},
                {'index': {'val': 1}, 'value': {'val': 200}},
            ]
            client.replace_log(
                log_id='LogUUID',
                log_points=points,
                index_unit='ft',
                value_unit='API'
            )
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
        Update metadata for a log.

        :param log_id: UUID of the log.
        :param name: Optional new name for the log.
        :param unit: Optional new unit of measure for the log values.
        :param headers: Optional additional HTTP headers.

        :return: True if the update was successful, False otherwise.

        :example:

        .. code-block:: python

            # Update log metadata
            success = client.update_log_meta(
                log_id='LogUUID',
                name='Log1',
                unit='API'
            )
            if success:
                print('Log metadata updated successfully')
        """
        url = f'logs/{log_id}'
        request_data = {'name': name, 'unit': unit}
        response = self._send_patch_request(url=url, request_data=request_data, headers=headers)

        return response.status_code == status_codes.ok

    def create_typewell_log(
        self, typewell_id: str, name: str, headers: Optional[Dict] = None
    ) -> PapiObjectCreationResult:
        """
        Create a new log in a type well.

        :param typewell_id: UUID of the type well.
        :param name: Name of the log.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiObjectCreationResult` containing the created object's ID.

        :example:

        .. code-block:: python

            # Create a new log in a type well
            result = client.create_typewell_log(
                typewell_id='TypewellUUID',
                name='Log1'
            )
            print(f'Created log with ID: {result.id}')
        """
        url = f'typewells/{typewell_id}/logs'
        request_data = {'name': name}

        return self._send_post_request(url=url, request_data=request_data, headers=headers)

    def fetch_traces(self, headers: Optional[Dict] = None):
        """
        Fetch all available traces.

        :param headers: Optional additional HTTP headers.

        :return: List of trace data.

        :example:

        .. code-block:: python

            # Fetch all available traces
            traces = client.fetch_traces()
        """
        data = self._send_request(
            url='traces',
            headers=headers,
        )

        return data['content']

    def fetch_well_mapped_traces(self, well_id: str, trace_type: TraceType, headers: Optional[Dict] = None):
        """
        Fetch mapped traces of a specific type for a well.

        :param well_id: UUID of the well.
        :param trace_type: Type of traces to fetch as :class:`~rogii_solo.papi.types.TraceType`.
        :param headers: Optional additional HTTP headers.

        :return: List of mapped trace data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.types import TraceType

            # Fetch mapped traces for a well
            traces = client.fetch_well_mapped_traces(
                well_id="well_uuid",
                trace_type=TraceType.TIME
            )
        """
        data = self._send_request(
            url=f'wells/{well_id}/traces/mapped/',
            params={'type': trace_type},
            headers=headers,
        )

        return data['content']

    def fetch_well_mapped_time_traces(self, well_id: str, headers: Optional[Dict] = None):
        """
        Fetch mapped time traces for a well.

        :param well_id: UUID of the well.
        :param headers: Optional additional HTTP headers.

        :return: List of mapped time trace data.

        :example:

        .. code-block:: python

            # Fetch mapped time traces for a well
            traces = client.fetch_well_mapped_time_traces(well_id='WellUUID')

        """
        return self.fetch_well_mapped_traces(well_id=well_id, trace_type='TIME', headers=headers)

    def fetch_well_mapped_calc_traces(self, well_id: str, headers: Optional[Dict] = None):
        """
        Fetch mapped calculated traces for a well.

        :param well_id: UUID of the well.
        :param headers: Optional additional HTTP headers.

        :return: List of mapped calculated trace data.

        :example:

        .. code-block:: python

            # Fetch mapped calculated traces for a well
            traces = client.fetch_well_mapped_calc_traces(well_id='WellUUID')

        """
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
        Fetch mapped calculated traces for a well.

        :param well_id: UUID of the well.
        :param trace_id: UUID of the trace.
        :param time_from: Start time of the trace.
        :param time_to: End time of the trace.
        :param trace_hash: Hash of the trace.
        :param limit: Limit the number of traces.
        :param headers: Optional additional HTTP headers.

        :return: List of mapped calculated trace data.

        :example:

        .. code-block:: python

            # Fetch time traces for a well
            traces = client.fetch_well_time_trace(well_id='WellUUID', trace_id='TraceUUID')

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
        Fetch mapped calculated traces for a well.

        :param well_id: UUID of the well.
        :param trace_id: UUID of the trace.
        :param time_from: Start time of the trace.
        :param time_to: End time of the trace.
        :param trace_hash: Hash of the trace.
        :param headers: Optional additional HTTP headers.

        :return: List of mapped calculated trace data.

        :example:

        .. code-block:: python

            # Fetch calculated traces for a well
            traces = client.fetch_well_calc_trace(well_id='WellUUID', trace_id='TraceUUID')

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
        """
        Update the metadata of a well.

        :param well_id: UUID of the well.
        :param name: Name of the well.
        :param operator: Operator of the well.
        :param api: API of the well.
        :param xsrf: XSRF of the well.
        :param ysrf: YSRF of the well.
        :param kb: KB of the well.
        :param azimuth: Azimuth of the well.
        :param convergence: Convergence of the well.
        :param tie_in_tvd: Tie in TVD of the well.
        :param tie_in_ns: Tie in NS of the well.
        :param tie_in_ew: Tie in EW of the well.
        :param headers: Optional additional HTTP headers.

        :example:

        .. code-block:: python

            # Update well metadata
            client.update_well_meta(well_id='WellUUID', name='Well1')
        """
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
        """
        Update the metadata of a type well.

        :param well_id: UUID of the type well.
        :param name: Name of the type well.
        :param operator: Operator of the type well.
        :param api: API of the type well.
        :param xsrf: XSRF of the type well.
        :param ysrf: YSRF of the type well.
        :param kb: KB of the type well.
        :param convergence: Convergence of the type well.
        :param tie_in_tvd: Tie in TVD of the type well.
        :param tie_in_ns: Tie in NS of the type well.
        :param tie_in_ew: Tie in EW of the type well.
        :param headers: Optional additional HTTP headers.

        :example:

        .. code-block:: python

            # Update type well metadata
            client.update_typewell_meta(well_id='WellUUID', name='Well1')
        """
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
        """
        Update the metadata of a well plan.

        :param well_id: UUID of the well plan.
        :param name: Name of the well plan.
        :param operator: Operator of the well plan.
        :param api: API of the well plan.
        :param xsrf: XSRF of the well plan.
        :param ysrf: YSRF of the well plan.
        :param kb: KB of the well plan.
        :param convergence: Convergence of the well plan.
        :param tie_in_tvd: Tie in TVD of the well plan.
        :param tie_in_ns: Tie in NS of the well plan.
        :param tie_in_ew: Tie in EW of the well plan.
        :param headers: Optional additional HTTP headers.

        :example:

        .. code-block:: python

            # Update well plan metadata
            client.update_nested_well_meta(well_id='WellPlanUUID', name='WellPlan1')
        """
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
        Create a well in the project

        :param project_id: UUID of the project.
        :param name: Name of the well.
        :param operator: Operator of the well.
        :param api: API of the well.
        :param xsrf: XSRF of the well.
        :param ysrf: YSRF of the well.
        :param kb: KB of the well.
        :param convergence: Convergence of the well.
        :param tie_in_tvd: Tie in TVD of the well plan.
        :param tie_in_ns: Tie in NS of the well plan.
        :param tie_in_ew: Tie in EW of the well plan.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiObjectCreationResult` object.

        :example:

        .. code-block:: python

            # Create a well
            client.create_well(project_id='ProjectUUID',
                name='Well1',
                operator='Operator1',
                api='API1',
                convergence=PapiVar(10),
                azimuth=PapiVar(20),
                kb=PapiVar(30),
                tie_in_tvd=PapiVar(40),
                tie_in_ns=PapiVar(50),
                tie_in_ew=PapiVar(60),
                xsrf_real=PapiVar(70),
                ysrf_real=PapiVar(80),
            )
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
        Create a type well in the project

        :param project_id: UUID of the project.
        :param name: Name of the type well.
        :param operator: Operator of the type well.
        :param api: API of the type well.
        :param xsrf: XSRF of the type well.
        :param ysrf: YSRF of the type well.
        :param kb: KB of the type well.
        :param convergence: Convergence of the type well.
        :param tie_in_tvd: Tie in TVD of the type well.
        :param tie_in_ns: Tie in NS of the type well.
        :param tie_in_ew: Tie in EW of the type well.
        :param headers: Optional additional HTTP headers.

        :return: :class:`PapiObjectCreationResult` object.

        :example:

        .. code-block:: python

            # Create a type well
            client.create_typewell(project_id='ProjectUUID',
                name='TypeWell1',
                operator='Operator1',
                api='API1',
                convergence=PapiVar(10),
                kb=PapiVar(30),
                tie_in_tvd=PapiVar(40),
                tie_in_ns=PapiVar(50),
                tie_in_ew=PapiVar(60),
                xsrf_real=PapiVar(70),
                ysrf_real=PapiVar(80),
            )
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

        :param well_id: UUID of the well.
        :param offset: Offset of the well linked typewells.
        :param limit: Limit of the well linked typewells.
        :param headers: Optional additional HTTP headers.

        :example:

        .. code-block:: python

            # Fetch well linked typewells
            client.fetch_well_linked_typewells(well_id='WellUUID')
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
        Fetches well comments

        :param well_id: UUID of the well.
        :param offset: Offset of the well comments.
        :param limit: Limit of the well comments.
        :param headers: Optional additional HTTP headers.

        :example:

        .. code-block:: python

            # Fetch well comments
            client.fetch_well_comments(well_id='WellUUID')
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
        Fetches well attributes

        :param well_id: UUID of the well.
        :param headers: Optional additional HTTP headers.

        :example:

        .. code-block:: python

            # Fetch well attributes
            client.fetch_well_attributes(well_id='WellUUID')
        """
        return self._send_request(
            url=f'wells/{well_id}/attributevalues',
            headers=headers,
        )

    def fetch_typewell(self, typewell_id: str, headers: Optional[Dict] = None):
        """
        Fetches type well data

        :param typewell_id: UUID of the type well.
        :param headers: Optional additional HTTP headers.

        :example:

        .. code-block:: python

            # Fetch type well data
            client.fetch_typewell(typewell_id='TypewellUUID')
        """
        return self._send_request(
            url=f'typewells/{typewell_id}/raw',
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
        """
        Replace well trajectory

        :param well_id: UUID of the well.
        :param md_uom: MD unit of measure.
        :param incl_uom: Inclination unit of measure.
        :param azi_uom: Azimuth unit of measure.
        :param trajectory_stations: :class:`PapiTrajectory` object.
        :param headers: Optional additional HTTP headers.

        :example:

        .. code-block:: python

            # Replace well trajectory
            client.replace_well_trajectory(
                well_id='WellUUID',
                md_uom='m',
                incl_uom='deg',
                azi_uom='deg',
                trajectory_stations=PapiTrajectory(),
            )
        """
        url = f'wells/{well_id}/trajectory'
        request_data = {
            'md_uom': md_uom,
            'incl_uom': incl_uom,
            'azi_uom': azi_uom,
            'trajectory_stations': trajectory_stations,
        }

        return self._send_put_request(url=url, request_data=request_data, headers=headers)

    def update_top_meta(self, top_id: str, name: str, md: PapiVar, headers: Optional[Dict] = None) -> bool:
        """
        Update top metadata

        :param top_id: UUID of the top.
        :param name: Name of the top.
        :param md: MD of the top.
        :param headers: Optional additional HTTP headers.

        :return: True if the top metadata was updated successfully, False otherwise.

        :example:

        .. code-block:: python

            # Replace well trajectory
            client.update_top_meta(
                top_id='TopUUID',
                name='Top1',
                md=PapiVar(1000),
            )
        """
        url = f'tops/{top_id}'
        request_data = {'name': name, 'md': md}
        response = self._send_patch_request(url=url, request_data=request_data, headers=headers)

        return response.status_code == status_codes.ok
