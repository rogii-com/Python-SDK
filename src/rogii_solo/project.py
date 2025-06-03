from datetime import datetime
from typing import Any, Dict, Optional

from pandas import DataFrame

from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.utils.objects import find_by_uuid
from rogii_solo.well import Typewell, Well


class Project(ComplexObject):
    """
    Represent a :class:`Project` from the collection of projects in the :class:`SoloClient`.

    :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get the unique ID of the Project
            project_uuid = project.uuid
            print(project_uuid)

            # Get the name of the Project
            project_name = project.name
            print(project_name)

            # Get the measurement unit of the Project
            project_measure_unit = project.measure_unit
            print(project_measure_unit)

            # Get the role associated with the Project
            project_role = project.role
            print(project_role)

            # Get the coordinate system of the Project
            project_geo_crs = project.geo_crs
            print(project_geo_crs)

            # Get the last accessed date of the Project
            project_accessed_on = project.accessed_on
            print(project_accessed_on)

            # Get the last modified date of the Project
            project_modified_on = project.modified_on
            print(project_modified_on)

            # Get the UUID of the global (parent) Project
            project_parent_uuid = project.parent_uuid
            print(project_parent_uuid)

            # Get the name of the global (parent) Project
            project_parent_name = project.parent_name
            print(project_parent_name)

            # Check if the Project is virtual
            project_is_virtual = project.virtual
            print(project_is_virtual)
    """

    def __init__(self, papi_client: PapiClient, **kwargs):
        super().__init__(papi_client)

        self.uuid: Optional[str] = None
        """Unique identifier for the :class:`Project`."""

        self.name: Optional[str] = None
        """Name of the :class:`Project`."""

        self.measure_unit: Optional[str] = None
        """Measurement unit used in the :class:`Project`."""

        self.role: Optional[str] = None
        """User's role in the :class:`Project`."""

        self.geo_crs: Optional[str] = None
        """Coordinate reference system used in the :class:`Project`."""

        self.accessed_on: Optional[datetime] = None
        """Last accessed date of the :class:`Project`."""

        self.modified_on: Optional[datetime] = None
        """Last modified date of the :class:`Project`."""

        self.parent_uuid: Optional[str] = None
        """UUID of the global (parent) :class:`Project` to which this Project belongs."""

        self.parent_name: Optional[str] = None
        """Name of the global (parent) :class:`Project` to which this Project belongs."""

        self.virtual: Optional[bool] = None
        """True if the :class:`Project` is virtual."""

        self.__dict__.update(kwargs)

        self._wells: Optional[ObjectRepository[Well]] = None
        self._typewells: Optional[ObjectRepository[Typewell]] = None

    @property
    def wells(self) -> ObjectRepository[Well]:
        """
        Get Wells of the :class:`Project`.

        :return: :class:`ObjectRepository` containing :class:`~well.Well` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get Wells of the Project
            wells = project.wells
            print(wells.to_dict())
        """
        if self._wells is None:
            self._wells = ObjectRepository(
                objects=[
                    Well(papi_client=self._papi_client, project=self, **item)
                    for item in self._papi_client.get_project_wells_data(project_id=self.uuid)
                ]
            )

        return self._wells

    @property
    def typewells(self) -> ObjectRepository[Typewell]:
        """
        Get Typewells of the :class:`Project`.

        :return: :class:`ObjectRepository` containing :class:`~well.Typewell` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get Typewells of the Project
            typewells = project.typewells
            print(typewells.to_dict())
        """
        if self._typewells is None:
            self._typewells = ObjectRepository(
                objects=[
                    Typewell(papi_client=self._papi_client, project=self, **item)
                    for item in self._papi_client.get_project_typewells_data(project_id=self.uuid)
                ]
            )

        return self._typewells

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`Project` instance to a dictionary.

        :return: Dictionary representation of the :class:`Project`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Convert the Project to a dictionary
            project_dict = project.to_dict()
            print(project_dict)
        """
        return {
            'uuid': self.uuid,
            'name': self.name,
            'measure_unit': self.measure_unit,
            'role': self.role,
            'geo_crs': self.geo_crs,
            'accessed_on': self.accessed_on,
            'modified_on': self.modified_on,
            'parent_uuid': self.parent_uuid,
            'parent_name': self.parent_name,
            'virtual': self.virtual,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`Project` instance to a Pandas DataFrame.

        :return: DataFrame representation of the :class:`Project`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Convert the Project to a DataFrame
            project_df = project.to_df()
            print(project_df)
        """
        return DataFrame([self.to_dict(get_converted)])

    def create_well(
        self,
        name: str,
        api: str,
        operator: str,
        convergence: float,
        azimuth: float,
        kb: float,
        tie_in_tvd: float,
        tie_in_ns: float,
        tie_in_ew: float,
        xsrf_real: float,
        ysrf_real: float,
    ):
        """
        Create well in the :class:`Project`.

        :param name: Name of the well.
        :param api: API of the well.
        :param operator: Operator of the well.
        :param convergence: Convergence of the well.
        :param azimuth: Azimuth of the well.
        :param kb: KB of the well.
        :param tie_in_tvd: Tie in TVD of the well.
        :param tie_in_ns: Tie in North-South direction coordinate of the well.
        :param tie_in_ew: Tie in East-West direction coordinate of the well.
        :param xsrf_real: Surface x-coordinate of the well.
        :param ysrf_real: Surface y-coordinate of the well.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Create 'Well1' in the Project
            project.create_well(
                name='Well1',
                api='001-123-1236',
                operator='Schl',
                convergence=0.1,
                azimuth=12,
                kb=132,
                tie_in_tvd=2456,
                tie_in_ns=145,
                tie_in_ew=1643,
                xsrf_real=643826,
                ysrf_real=83461678,
            )
            print(project.wells.find_by_name('Well1').to_dict())
        """
        well_id = self._papi_client.create_well(
            project_id=self.uuid,
            name=name,
            operator=operator,
            api=api,
            convergence=self._papi_client.prepare_papi_var(convergence),
            azimuth=self._papi_client.prepare_papi_var(azimuth),
            kb=self._papi_client.prepare_papi_var(kb),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew),
            xsrf_real=self._papi_client.prepare_papi_var(xsrf_real),
            ysrf_real=self._papi_client.prepare_papi_var(ysrf_real),
        )
        well_data = self._papi_client.get_project_well_data(well_id=well_id['uuid'])

        if self._wells is not None:
            self._wells.append(Well(papi_client=self._papi_client, project=self, **well_data))

    def create_typewell(
        self,
        name: str,
        operator: str,
        api: str,
        convergence: float,
        kb: float,
        tie_in_tvd: float,
        tie_in_ns: float,
        tie_in_ew: float,
        xsrf_real: float,
        ysrf_real: float,
    ):
        """
        Create typewell in the :class:`Project`.

        :param name: Name of the typewell.
        :param operator: Operator of the typewell.
        :param api: API of the typewell.
        :param convergence: Convergence of the typewell.
        :param kb: KB of the typewell.
        :param tie_in_tvd: Tie in TVD of the typewell.
        :param tie_in_ns: Tie in North-South direction coordinate of the typewell.
        :param tie_in_ew: Tie in East-West direction coordinate of the typewell.
        :param xsrf_real: Surface x-coordinate of the typewell.
        :param ysrf_real: Surface y-coordinate of the typewell.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Create 'Typewell1' in the Project
            project.create_typewell(
                name='Typewell1',
                api='001-123-1236',
                operator='Schl',
                convergence=0.1,
                azimuth=12,
                kb=132,
                tie_in_tvd=2456,
                tie_in_ns=145,
                tie_in_ew=1643,
                xsrf_real=643826,
                ysrf_real=83461678,
            )
            print(project.typewells.find_by_name('Typewell1').to_dict())
        """
        typewell_id = self._papi_client.create_typewell(
            project_id=self.uuid,
            name=name,
            operator=operator,
            api=api,
            convergence=self._papi_client.prepare_papi_var(convergence),
            kb=self._papi_client.prepare_papi_var(kb),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew),
            xsrf_real=self._papi_client.prepare_papi_var(xsrf_real),
            ysrf_real=self._papi_client.prepare_papi_var(ysrf_real),
        )
        # No raw method for typewell
        typewell_data = find_by_uuid(
            value=typewell_id['uuid'],
            input_list=self._papi_client.get_project_typewells_data(project_id=self.uuid, query=name),
        )

        if self._typewells is not None:
            self._typewells.append(Typewell(papi_client=self._papi_client, project=self, **typewell_data))
