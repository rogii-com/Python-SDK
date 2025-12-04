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
    """
    :class:`PapiClient` connect SoloClient with the server to get data from the Solo API.

    :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)

            # Get List of global projects dictionary representation
            projects = client.get_global_projects_data()
            print(projects)
    """

    def __init__(self, settings_auth: SettingsAuth):
        app_id = base64.standard_b64encode(PYTHON_SDK_APP_ID.encode()).decode()
        """App ID"""

        fingerprint = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
        """ A unique SHA-256 hash string"""

        headers = {
            'User-Agent': f'PythonSDK/{__version__}',
            'X-Solo-Hid': f'{fingerprint}:{app_id}',
        }
        """Headers for the request"""

        papi_url = urljoin(settings_auth.papi_domain_name, SOLO_PAPI_URL)
        """PAPI URL"""

        papi_auth_url = urljoin(settings_auth.papi_domain_name, SOLO_OPEN_AUTH_SERVICE_URL)
        """PAPI Auth URL"""

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
        Create a dictionary representation of a value for PAPI.

        :param value: The value to convert to PAPI format.

        :return: A :class:`PapiVar` representation of the value.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)

            azimuth = 45
            papi_var = client.prepare_papi_var(azimuth)
        """
        if isinstance(value, str):
            return value

        if value is None:
            return {'undefined': True}

        return {'val': value}

    def parse_papi_data(self, data: Any, default: Any = None) -> Any:
        """
        Parse PAPI data structures.

        :param data: The PAPI data structure to parse.
        :param default: Default value to use for undefined PAPI variables.

        :return: The parsed data structure.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)

            # Get Earth Model Sections data
            earth_model_uuid = 'EarthModelUUID'

            for uuid, section_data in client.fetch_earth_model_sections(earth_model_id=earth_model_uuid).items():
                section_data = client.parse_papi_data(section_data)
                print(section_data)
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
        """
        Get a list of all global projects.

        :return: List of Dictionaries of global projects.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)

            # Get List of global projects dictionary representation
            projects = client.get_global_projects_data()
            print(projects)
        """
        return list(self._gen_data_page(func=self.fetch_projects, **kwargs))

    def get_virtual_projects_data(self, **kwargs) -> PapiDataList:
        """
        Get a list of all virtual projects.

        :return: List of Dictionaries of virtual project data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)

            # Get List of virtual projects dictionary representation
            projects = client.get_virtual_projects_data()
            print(projects)
        """
        return list(self._gen_data_page(func=self.fetch_virtual_projects, **kwargs))

    def get_project_wells_data(self, project_id: str, **kwargs) -> PapiDataList:
        """
        Get a list of wells for a specific project.

        :param project_id: UUID of the project.

        :return: List of Dictionaries of well data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            project_id = 'ProjectUUID'

            # Get List of wells for a specific project
            wells = client.get_project_wells_data(project_id=project_id)
            print(wells)
        """
        return list(self._gen_data_page(func=self.fetch_project_raw_wells, project_id=project_id, **kwargs))

    def get_project_well_data(self, well_id: str, **kwargs) -> PapiData:
        """
        Get data for a specific well.

        :param well_id: UUID of the well.

        :return: Dictionary representation of well data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get data for a specific well
            well = client.get_project_well_data(well_id=well_id)
            print(well)
        """
        return self.parse_papi_data(self.fetch_raw_well(well_id=well_id, **kwargs))

    def get_well_trajectory_data(self, well_id: str, **kwargs) -> PapiDataList:
        """
        Get trajectory data for a specific well.

        :param well_id: UUID of the well.

        :return: List of Dictionaries of trajectory data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get trajectory data for a specific well
            trajectory_data = client.get_well_trajectory_data(well_id=well_id)
            print(trajectory_data)
        """
        return [
            self.parse_papi_data(data_item) for data_item in self.fetch_well_raw_trajectory(well_id=well_id, **kwargs)
        ]

    def get_well_interpretations_data(self, well_id: str, **kwargs) -> PapiDataList:
        """
        Get interpretations for a specific well.

        :param well_id: UUID of the well.

        :return: List of interpretation data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get interpretations for a specific well
            interpretations = client.get_well_interpretations_data(well_id=well_id)
            print(interpretations)
        """
        return list(self._gen_data_page(func=self.fetch_well_raw_interpretations, well_id=well_id, **kwargs))

    def get_interpretation_horizons_data(self, interpretation_id: str, **kwargs) -> PapiDataList:
        """
        Get horizons for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.

        :return: List of horizon data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            interpretation_id = 'InterpretationUUID'

            # Get horizons for a specific interpretation
            horizons = client.get_interpretation_horizons_data(interpretation_id=interpretation_id)
            print(horizons)
        """
        return list(
            self._gen_data_page(func=self.fetch_interpretation_horizons, interpretation_id=interpretation_id, **kwargs)
        )

    def get_interpretation_earth_models_data(self, interpretation_id: str, **kwargs) -> PapiDataList:
        """
        Get earth models for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.

        :return: List of earth model data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            interpretation_id = 'InterpretationUUID'

            # Get earth models for a specific interpretation
            earth_models = client.get_interpretation_earth_models_data(interpretation_id=interpretation_id)
            print(earth_models)
        """
        return list(
            self._gen_data_page(
                func=self.fetch_interpretation_earth_models, interpretation_id=interpretation_id, **kwargs
            )
        )

    def get_interpretation_tvt_data(self, interpretation_id: str, **kwargs) -> PapiDataList:
        """
        Get TVT (True Vertical Thickness) data for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.

        :return: List of TVT data points.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            interpretation_id = 'InterpretationUUID'

            # Get TVT data for a specific interpretation
            tvt_data = client.get_interpretation_tvt_data(interpretation_id=interpretation_id)
            print(tvt_data)
        """
        return [
            self.parse_papi_data(tvt_data)
            for tvt_data in self.fetch_interpretation_horizons_data(interpretation_id=interpretation_id, **kwargs)
        ]

    def get_interpretation_assembled_segments_data(self, interpretation_id: str, **kwargs) -> PapiData:
        """
        Get assembled segments for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.

        :return: Dictionary containing horizons and segments data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            interpretation_id = 'InterpretationUUID'

            # Get assembled segments for a specific interpretation
            assembled_segments = client.get_interpretation_assembled_segments_data(interpretation_id=interpretation_id)
            print(assembled_segments)
        """
        assembled_segments = self.fetch_interpretation_assembled_segments(interpretation_id=interpretation_id, **kwargs)

        return {
            'horizons': self.parse_papi_data(assembled_segments['horizons']),
            'segments': self.parse_papi_data(assembled_segments['segments']),
        }

    def get_interpretation_starred_horizons(self, interpretation_id: str, **kwargs) -> PapiStarredHorizons:
        """
        Get starred horizons for a specific interpretation.

        :param interpretation_id: UUID of the interpretation.

        :return: :class:`PapiStarredHorizons` containing starred horizons UUIDs.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            interpretation_id = 'InterpretationUUID'

            # Get starred horizons for a specific interpretation
            starred_horizons = client.get_interpretation_starred_horizons(interpretation_id=interpretation_id)
            print(starred_horizons)
        """
        starred_horizons = self.fetch_interpretation_starred_horizons(interpretation_id=interpretation_id, **kwargs)

        return PapiStarredHorizons(
            top=starred_horizons['top'], center=starred_horizons['center'], bottom=starred_horizons['bottom']
        )

    def get_well_target_lines_data(self, well_id: str, **kwargs) -> PapiDataList:
        """
        Get target lines for a specific well.

        :param well_id: UUID of the well.

        :return: List of target line data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get target lines for a specific well
            target_lines = client.get_well_target_lines_data(well_id=well_id)
            print(target_lines)
        """
        return list(self._gen_data_page(func=self.fetch_well_target_lines, well_id=well_id, **kwargs))

    def get_well_nested_wells_data(self, well_id: str, **kwargs) -> PapiDataList:
        """
        Get nested wells for a specific well.

        :param well_id: UUID of the well.

        :return: List of nested well data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get nested wells for a specific well
            nested_wells = client.get_well_nested_wells_data(well_id=well_id)
            print(nested_wells)
        """
        return list(self._gen_data_page(func=self.fetch_well_nested_wells, well_id=well_id, **kwargs))

    def get_nested_well_trajectory_data(self, nested_well_id: str, **kwargs) -> PapiDataList:
        """
        Get trajectory data for a specific nested well.

        :param nested_well_id: UUID of the nested well.

        :return: List of trajectory points.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            nested_well_id = 'NestedWellUUID'

            # Get trajectory data for a specific nested well
            trajectory_data = client.get_nested_well_trajectory_data(nested_well_id=nested_well_id)
            print(trajectory_data)
        """
        return [
            self.parse_papi_data(data_item)
            for data_item in self.fetch_nested_well_raw_trajectory(nested_well_id=nested_well_id, **kwargs)
        ]

    def get_well_logs_data(self, well_id: str, **kwargs) -> PapiDataList:
        """
        Get logs for a specific well.

        :param well_id: UUID of the well.

        :return: List of log data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get logs for a specific well
            logs = client.get_well_logs_data(well_id=well_id)
            print(logs)
        """
        return list(self._gen_data_page(func=self.fetch_well_logs, well_id=well_id, **kwargs))

    def get_typewell_logs_data(self, typewell_id: str, **kwargs) -> PapiDataList:
        """
        Get logs for a specific type well.

        :param typewell_id: UUID of the type well.

        :return: List of log data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            typewell_id = 'TypewellUUID'

            # Get logs for a specific type well
            logs = client.get_typewell_logs_data(typewell_id=typewell_id)
            print(logs)
        """
        return list(self._gen_data_page(func=self.fetch_typewell_logs, typewell_id=typewell_id, **kwargs))

    def get_log_points(self, log_id: str) -> PapiDataList:
        """
        Get data points for a specific log.

        :param log_id: UUID of the log.

        :return: List of log data points.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            log_id = 'LogUUID'

            # Get data points for a specific log
            log_points = client.get_log_points(log_id=log_id)
            print(log_points)
        """
        return [self.parse_papi_data(data_item) for data_item in self.fetch_log_points(log_id=log_id)]

    def get_project_typewells_data(self, project_id: str, **kwargs) -> PapiDataList:
        """
        Get type wells for a specific project.

        :param project_id: UUID of the project.

        :return: List of type well data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            project_id = 'ProjectUUID'

            # Get type wells for a specific project
            typewells = client.get_project_typewells_data(project_id=project_id)
            print(typewells)
        """
        return list(self._gen_data_page(func=self.fetch_project_typewells, project_id=project_id, **kwargs))

    def get_typewell_trajectory_data(self, typewell_id: str, **kwargs) -> PapiDataList:
        """
        Get trajectory data for a specific type well.

        :param typewell_id: UUID of the type well.

        :return: List of trajectory points.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            typewell_id = 'TypewellUUID'

            # Get trajectory data for a specific type well
            trajectory_data = client.get_typewell_trajectory_data(typewell_id=typewell_id)
            print(trajectory_data)
        """
        return [
            self.parse_papi_data(data_item)
            for data_item in self.fetch_typewell_raw_trajectory(typewell_id=typewell_id, **kwargs)
        ]

    def get_well_topsets_data(self, well_id: str, **kwargs) -> PapiDataList:
        """
        Get topsets for a specific well.

        :param well_id: UUID of the well.

        :return: List of topset data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get topsets for a specific well
            topsets = client.get_well_topsets_data(well_id=well_id)
            print(topsets)
        """
        return list(self._gen_data_page(func=self.fetch_well_topsets, well_id=well_id, **kwargs))

    def get_typewell_topsets_data(self, typewell_id: str, **kwargs) -> PapiDataList:
        """
        Get topsets for a specific type well.

        :param typewell_id: UUID of the type well.

        :return: List of topset data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            typewell_id = 'TypewellUUID'

            # Get topsets for a specific type well
            topsets = client.get_typewell_topsets_data(typewell_id=typewell_id)
            print(topsets)
        """
        return list(self._gen_data_page(func=self.fetch_typewell_topsets, typewell_id=typewell_id, **kwargs))

    def get_nested_well_topsets_data(self, nested_well_id: str, **kwargs) -> PapiDataList:
        """
        Get topsets for a specific nested well.

        :param nested_well_id: UUID of the nested well.

        :return: List of topset data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            nested_well_id = 'NestedWellUUID'

            # Get topsets for a specific nested well
            topsets = client.get_nested_well_topsets_data(nested_well_id=nested_well_id)
            print(topsets)
        """
        return list(self._gen_data_page(func=self.fetch_nested_well_topsets, nested_well_id=nested_well_id, **kwargs))

    def get_topset_tops_data(self, topset_id: str, **kwargs) -> PapiDataList:
        """
        Get tops for a specific topset.

        :param topset_id: UUID of the topset.

        :return: List of top data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            topset_id = 'TopsetUUID'

            # Get tops for a specific topset
            tops = client.get_topset_tops_data(topset_id=topset_id)
            print(tops)
        """
        return list(self._gen_data_page(func=self.fetch_topset_tops, topset_id=topset_id, **kwargs))

    def get_topset_starred_tops(self, topset_id: str, **kwargs) -> PapiStarredTops:
        """
        Get starred tops for a specific topset.

        :param topset_id: UUID of the topset.

        :return: :class:`PapiStarredTops` containing starred top UUIDs.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            topset_id = 'TopsetUUID'

            # Get starred tops for a specific topset
            topsets = client.get_topset_starred_tops(topset_id=topset_id)
            print(topsets)
        """
        starred_tops = self.fetch_topset_starred_tops(topset_id=topset_id, **kwargs)

        return PapiStarredTops(top=starred_tops['top'], center=starred_tops['center'], bottom=starred_tops['bottom'])

    def get_well_mudlogs_data(self, well_id: str, **kwargs) -> PapiDataList:
        """
        Get mudlogs for a specific well.

        :param well_id: UUID of the well.

        :return: List of mudlog data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get mudlogs for a specific well
            mudlogs = client.get_well_mudlogs_data(well_id=well_id)
            print(mudlogs)
        """
        return list(self._gen_data_page(func=self.fetch_well_mudlogs, well_id=well_id, **kwargs))

    def get_typewell_mudlogs_data(self, typewell_id: str, **kwargs) -> PapiDataList:
        """
        Get mudlogs for a specific type well.

        :param typewell_id: UUID of the type well.

        :return: List of mudlog data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            typewell_id = 'TypewellUUID'

            # Get mudlogs for a specific type well
            mudlogs = client.get_typewell_mudlogs_data(typewell_id=typewell_id)
            print(mudlogs)
        """
        return list(self._gen_data_page(func=self.fetch_typewell_mudlogs, typewell_id=typewell_id, **kwargs))

    def get_mudlog_data(self, mudlog_id: str) -> PapiDataList:
        """
        Get data for a specific mudlog.

        :param mudlog_id: UUID of the mudlog.

        :return: List of mudlog data points.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            mudlog_id = 'MudlogUUID'

            # Get mudlogs for a specific mudlog
            mudlogs = client.get_mudlog_data(mudlog_id=mudlog_id)
            print(mudlogs)
        """
        return [self.parse_papi_data(data_item) for data_item in self.fetch_mudlog_logs(mudlog_id)]

    def get_traces(self, **kwargs) -> PapiDataList:
        """
        Get all available traces.

        :param kwargs: Additional parameters to pass to the fetch request.

        :return: List of trace data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)

            # Get traces
            traces = client.get_traces()
            print(traces)
        """
        return self.fetch_traces(**kwargs)

    def get_well_mapped_time_traces_data(self, well_id: str, **kwargs) -> PapiDataList:
        """
        Get mapped time traces for a specific well.

        :param well_id: UUID of the well.

        :return: List of mapped time trace data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get mapped time traces for a specific well
            traces = client.get_well_mapped_time_traces_data(well_id=well_id)
            print(traces)
        """
        return self.fetch_well_mapped_time_traces(well_id=well_id, **kwargs)

    # TODO Change to default _gen_data_page when offset will be added to the endpoint
    def get_well_time_trace_data(self, well_id: str, trace_id: str, **kwargs) -> PapiDataList:
        """
        Get time trace data for a specific well.

        :param well_id: UUID of the well.
        :param trace_id: UUID of the trace.

        :return: List of time trace data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'
            trace_id = 'TraceUUID'

            # Get time trace data for a specific well
            traces = client.get_well_time_trace_data(well_id=well_id, trace_id=trace_id)
            print(traces)
        """

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
        """
        Get mapped calc traces for a specific well.

        :param well_id: UUID of the well.

        :return: List of mapped calc trace data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get mapped calc traces for a specific well
            traces = client.get_well_mapped_calc_traces_data(well_id=well_id)
            print(traces)
        """
        return self.fetch_well_mapped_calc_traces(well_id=well_id, **kwargs)

    def get_well_calc_trace_data(self, well_id: str, trace_id: str, **kwargs) -> PapiDataList:
        """
        Get calc trace data for a specific well.

        :param well_id: UUID of the well.
        :param trace_id: UUID of the trace.

        :return: List of calc trace data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'
            trace_id = 'TraceUUID'

            # Get calc trace data for a specific well
            traces = client.get_well_calc_trace_data(well_id=well_id, trace_id=trace_id)
            print(traces)
        """
        return self.fetch_well_calc_trace(well_id=well_id, trace_id=trace_id, **kwargs)

    def get_well_linked_typewells_data(self, **kwargs) -> PapiDataList:
        """
        Get linked type wells for a specific well.

        :param kwargs: Additional parameters to pass to the fetch request.

        :return: List of linked type wells data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get linked type wells for a specific well
            linked_typewells = client.get_well_linked_typewells_data(well_id=well_id)
            print(linked_typewells)
        """
        return list(self._gen_data_page(func=self.fetch_well_linked_typewells, **kwargs))

    def get_well_comments_data(self, well_id: str, **kwargs) -> PapiDataList:
        """
        Get comments for a specific well.

        :param well_id: UUID of the well.

        :return: List of comments data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get comments for a specific well
            comments = client.get_well_comments_data(well_id=well_id)
            print(comments)
        """
        return list(self._gen_data_page(func=self.fetch_well_comments, well_id=well_id, **kwargs))

    def get_well_attributes(self, well_id: str, **kwargs) -> PapiData:
        """
        Get attributes for a specific well.

        :param well_id: UUID of the well.

        :return: Well's attributes data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            well_id = 'WellUUID'

            # Get attributes for a specific well
            attributes = client.get_well_attributes(well_id=well_id)
            print(attributes)
        """
        return self.parse_papi_data(self.fetch_well_attributes(well_id=well_id, **kwargs))

    def get_typewell_data(self, typewell_id: str, **kwargs) -> PapiData:
        """
        Get data for a specific type well.

        :param typewell_id: UUID of the type well.

        :return: Type well data.

        :example:

        .. code-block:: python

            from rogii_solo.papi.client import PapiClient
            from rogii_solo.papi.types import SettingsAuth

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret
            papi_domain_name = ... # Input your papi domain name
            proxies = ... # Input your proxy or None

            client_auth = SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                papi_domain_name=papi_domain_name,
                proxies=None
            )
            client = PapiClient(client_auth)
            typewell_id = 'TypewellUUID'

            # Get data for a specific type well
            typewell = client.get_typewell_data(typewell_id=typewell_id)
            print(typewell)
        """
        return self.parse_papi_data(self.fetch_typewell(typewell_id=typewell_id, **kwargs))

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
