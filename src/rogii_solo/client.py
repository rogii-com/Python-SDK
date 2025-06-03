from typing import Optional

from rogii_solo.base import ObjectRepository
from rogii_solo.exceptions import InvalidProjectException, ProjectNotFoundException
from rogii_solo.papi.client import PapiClient
from rogii_solo.papi.types import ProxyData, SettingsAuth
from rogii_solo.project import Project
from rogii_solo.types import DataList
from rogii_solo.utils.constants import SOLO_PAPI_DEFAULT_DOMAIN_NAME


class SoloClient:
    """
    Main object for retrieving Solo PAPI data

    :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)

            # Get 'Project1' project
            project = solo_client.set_project_by_name('Project1')
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        papi_domain_name: str = SOLO_PAPI_DEFAULT_DOMAIN_NAME,
        proxies: Optional[ProxyData] = None,
    ):
        self._papi_client = PapiClient(
            SettingsAuth(
                client_id=client_id, client_secret=client_secret, papi_domain_name=papi_domain_name, proxies=proxies
            )
        )

        self._projects: Optional[ObjectRepository[Project]] = None
        self.project: Optional[Project] = None
        """Project of the :class:`SoloClient` defined by user via set method."""

    @property
    def projects(self) -> ObjectRepository[Project]:
        """
        Get projects of the :class:`SoloClient`.

        :return: :class:`~rogii_solo.base.ObjectRepository` containing :class:`~rogii_solo.project.Project` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            # Get client's projects
            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.projects
            print(projects.to_dict())
        """

        if self._projects is None:
            self._projects = ObjectRepository(
                objects=[Project(papi_client=self._papi_client, **item) for item in self._get_projects_data()]
            )

        return self._projects

    def _get_projects_data(self) -> DataList:
        global_projects_data = self._papi_client.get_global_projects_data()
        virtual_projects_data = self._papi_client.get_virtual_projects_data()

        return global_projects_data + virtual_projects_data

    def set_project_by_id(self, project_id: str) -> Optional[Project]:
        """
        Set and Get :class:`~rogii_solo.project.Project` by id.

        :return: :class:`~rogii_solo.project.Project` with the specified id.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            # Get 'ProjectID' project
            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_id('ProjectID')
            print(project.to_dict())
        """
        project = self.projects.find_by_id(project_id)

        if project is None:
            raise ProjectNotFoundException('Project not found.')

        return self.set_project(project)

    def set_project_by_name(self, project_name: str) -> Optional[Project]:
        """
        Set and Get :class:`~rogii_solo.project.Project` by name.

        :return: :class:`~rogii_solo.project.Project` with the specified name.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            # Get 'Project1' project
            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            print(project.to_dict())
        """

        project = self.projects.find_by_name(project_name)

        if project is None:
            raise ProjectNotFoundException('Project not found.')

        return self.set_project(project)

    def set_project(self, project: Project) -> Optional[Project]:
        """
        Set and Get :class:`~rogii_solo.project.Project` by :class:`~rogii_solo.project.Project`.

        :return: :class:`~rogii_solo.project.Project`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            # Get 'Project1' project
            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Set project
            project = set_project(project)
            print(project.to_dict())
        """

        if not isinstance(project, Project):
            raise InvalidProjectException('Must be the "Project" instance.')

        self.project = project

        return self.project
