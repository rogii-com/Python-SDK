from typing import Dict, List, Optional

from python_sdk.papi.client import PapiClient
from python_sdk.project import Project

from .base import ObjectRepository
from .exceptions import ProjectNotFoundException
from .types import SettingsAuth
from .utils.constants import SOLO_PAPI_DEFAULT_DOMAIN_NAME


class SoloClient:
    """
    Main object for retrieving Solo PAPI data
    """
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

        self._projects_data: List[Dict] = []
        self._projects: ObjectRepository[Project] = ObjectRepository(dicts=[], objects=[])
        self.project: Optional[Project] = None

    @property
    def projects_data(self) -> List[Dict]:
        if not self._projects_data:
            self._projects_data = [
                self._papi_client._parse_papi_data(project)
                for project in self._papi_client._request_all_pages_with_content(func=self._papi_client.fetch_projects)
            ]

        return self._projects_data

    @property
    def projects(self) -> ObjectRepository[Project]:
        if not self._projects:
            self._projects = ObjectRepository(
                dicts=self.projects_data,
                objects=[Project(papi_client=self._papi_client, **item) for item in self.projects_data]
            )

        return self._projects

    def set_project_by_id(self, project_id: str):
        self.project = self.projects.find_by_id(project_id)

        if not self.project:
            raise ProjectNotFoundException('Project not found.')

    def set_project_by_name(self, project_name: str):
        self.project = self.projects.find_by_name(project_name)

        if not self.project:
            raise ProjectNotFoundException('Project not found.')

    def replace_nested_well_trajectory(self,
                                       nested_well_id: str,
                                       md_uom: str,
                                       incl_uom: str,
                                       azi_uom: str,
                                       trajectory_stations: list
                                       ):
        wrapped_trajectory_stations = [
            {key: self._papi_client._prepare_papi_var(value) for key, value in point.items()}
            for point in trajectory_stations
        ]

        # FIXME: temporary fix for SOLO-5351
        fixed_wrapped_trajectory_stations = [
            {key if key != 'azim' else 'azi': value for key, value in point.items()}
            for point in wrapped_trajectory_stations
        ]

        return self._papi_client.replace_nested_well_trajectory(
            nested_well_id=nested_well_id,
            md_uom=md_uom,
            incl_uom=incl_uom,
            azi_uom=azi_uom,
            trajectory_stations=fixed_wrapped_trajectory_stations
        )
