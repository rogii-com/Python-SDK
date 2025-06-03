from typing import Any, Dict, Optional, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.calculations.converters import feet_to_meters
from rogii_solo.exceptions import InvalidTopDataException
from rogii_solo.papi.client import PapiClient
from rogii_solo.papi.types import PapiStarredTops
from rogii_solo.utils.objects import find_by_uuid

WellType = Union['rogii_solo.well.Well', 'rogii_solo.well.Typewell', 'rogii_solo.well.NestedWell']


class Topset(ComplexObject):
    """
    Represent a :class:`Topset` within a :class:`~rogii_solo.well.Well`, :class:`~rogii_solo.well.Typewell`, or
    :class:`~rogii_solo.well.NestedWell`. A :class:`Topset` is a collection of :class:`Top` objects that mark specific
    measured depths (MD) in a well, typically used to identify formation boundaries or other significant points.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')

        # Get TopSets of the Well
        topsets = well.topsets

        # Get a TopSet name
        topset = topsets.find_by_name('TopSet1')
        print(topset.name)

        # Get a TopSet id
        topset = topsets.find_by_id('TopSetID')
        print(topset.comment_id)
    """

    def __init__(self, papi_client: PapiClient, well: WellType, **kwargs):
        super().__init__(papi_client)

        self.well: WellType = well
        """The well object that contains this topset"""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`Topset`"""

        self.name: Optional[str] = None
        """Name of the :class:`Topset`"""

        self.__dict__.update(kwargs)

        self._tops: Optional[ObjectRepository[Top]] = None
        self._starred_tops_data: Optional[PapiStarredTops] = None
        self._starred_top_top: Optional[Top] = None
        self._starred_top_center: Optional[Top] = None
        self._starred_top_bottom: Optional[Top] = None

    @property
    def tops(self) -> ObjectRepository['Top']:
        """
        Get the Tops (MD/TVD points) associated with this :class:`Topset`.

        :return: :class:`~rogii_solo.base.ObjectRepository` containing :class:`Top` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')

            # Get all tops in the topset
            tops = topset.tops

            # Find a specific top by name
            formation_top = tops.find_by_name('Formation1')

            # Convert all tops to a dictionary
            tops_data = tops.to_dict()

            # Convert all tops to a DataFrame
            tops_df = tops.to_df()
        """
        if self._tops is None:
            self._tops = ObjectRepository(
                objects=[
                    Top(papi_client=self._papi_client, topset=self, **item)
                    for item in self._papi_client.get_topset_tops_data(topset_id=self.uuid)
                ]
            )

        return self._tops

    @property
    def starred_top_top(self) -> Optional['Top']:
        """
        Get the top starred Top of the :class:`Topset`.

        :return: The top :class:`Top` instance.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')

            # Get the top starred Top
            top = topset.starred_top_top
            if top:
                print(f'Top marker: {top.name} at MD {top.md}')
        """
        if self._starred_top_top is None:
            starred_tops_data = self._get_starred_tops_data()
            self._starred_top_top = self.tops.find_by_id(starred_tops_data['top'])

        return self._starred_top_top

    @property
    def starred_top_center(self) -> Optional['Top']:
        """
        Get the center starred Top of the :class:`Topset`.

        :return: The center :class:`Top` instance.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')

            # Get the center starred Top
            top = topset.starred_top_center

            if top:
                print(f'Center marker: {top.name} at MD {top.md}')
        """
        if self._starred_top_center is None:
            starred_tops_data = self._get_starred_tops_data()
            self._starred_top_center = self.tops.find_by_id(starred_tops_data['center'])

        return self._starred_top_center

    @property
    def starred_top_bottom(self) -> Optional['Top']:
        """
        Get the bottom starred Top of the :class:`Topset`.

        :return: The bottom :class:`Top` instance.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')

            # Get the bottom starred Top
            top = topset.starred_top_bottom

            if top:
                print(f'Bottom marker: {top.name} at MD {top.md}')
        """
        if self._starred_top_bottom is None:
            starred_tops_data = self._get_starred_tops_data()
            self._starred_top_bottom = self.tops.find_by_id(starred_tops_data['bottom'])

        return self._starred_top_bottom

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`Topset` instance to a dictionary.

        :param get_converted: (Optional) Whether to convert values to project units. Default is True.
        :return: Dictionary representation of the :class:`Topset`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')

            # Convert the Topset to a dictionary
            topset_dict = topset.to_dict()
            print(topset_dict)
        """
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`Topset` instance to a Pandas DataFrame.

        :param get_converted: (Optional) Whether to convert values to project units. Default is True.
        :return: DataFrame representation of the :class:`Topset`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')

            # Convert the TopSet to a DataFrame
            topset_df = topset.to_df()
            print(topset_df)
        """
        return DataFrame([self.to_dict(get_converted)])

    def create_top(self, name: str, md: float):
        """
        Create a new :class:`Top` in this :class:`Topset`.

        :param name: Name of the new top
        :param md: Measured depth (MD) of the new top
        :raises InvalidTopDataException: If the MD value is outside the valid range (0-100000)

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')

            # Create a new top at MD 1000.0
            topset.create_top(name='Formation1', md=1000.0)
        """
        if not 0 <= md <= 100000:
            raise InvalidTopDataException

        top_id = self._papi_client.create_topset_top(
            topset_id=self.uuid, name=name, md=self._papi_client.prepare_papi_var(md)
        )

        # No raw method for top
        top_data = find_by_uuid(
            value=top_id['uuid'], input_list=self._papi_client.get_topset_tops_data(topset_id=self.uuid)
        )

        if self._tops is not None:
            self._tops.append(Top(topset=self, **top_data))

    def _get_starred_tops_data(self):
        if self._starred_tops_data is None:
            self._starred_tops_data = self._papi_client.get_topset_starred_tops(self.uuid)

        return self._starred_tops_data


class Top(ComplexObject):
    """
    Represent a :class:`Top` within a :class:`Topset`. A :class:`Top` marks a specific measured depth (MD)
    in a well, typically used to identify formation boundaries or other significant points.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        topset = well.topsets.find_by_name('Topset1')

        # Create a new top
        topset.create_top(name='Formation1', md=1000.0)

        # Get the top by name
        top = topset.tops.find_by_name('Formation1')
    """

    def __init__(self, papi_client: PapiClient, topset: Topset, **kwargs):
        super().__init__(papi_client)

        self.topset: Topset = topset
        """The :class:`Topset` that contains this top"""

        self.measure_units: str = topset.well.project.measure_unit
        """The measurement units used for this top"""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`Top`"""

        self.name: Optional[str] = None
        """Name of the :class:`Top`"""

        self.md: Optional[float] = None
        """Measured depth (MD) of the :class:`Top`"""

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`Top` instance to a dictionary.

        :param get_converted: (Optional) Whether to convert values to project units. Default is True.
        :return: Dictionary representation of the :class:`Top`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')
            top = topset.tops.find_by_name('Formation1')

            # Convert the Top to a dictionary in project units
            top_dict = top.to_dict()
            print(top_dict)

            # Convert the Top to a dictionary without unit conversion
            top_dict = top.to_dict(get_converted=False)
            print(top_dict)
        """
        return {
            'uuid': self.uuid,
            'name': self.name,
            # MD is returned in project units
            'md': self.md if get_converted else feet_to_meters(self.md),
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`Top` instance to a Pandas DataFrame.

        :param get_converted: (Optional) Whether to convert values to project units. Default is True.
        :return: DataFrame representation of the :class:`Top`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')
            top = topset.tops.find_by_name('Formation1')

            # Convert the Top to a DataFrame
            top_df = top.to_df()
            print(top_df)
        """
        return DataFrame([self.to_dict(get_converted)])

    def update_meta(self, name: str, md: float):
        """
        Update the metadata of this :class:`Top`.

        :param name: Name for the :class:`Top`
        :param md: Measured depth (MD) for the :class:`Top`
        :raises InvalidTopDataException: If the MD value is outside the valid range (0-100000)
        :return: updated :class:`Top`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            topset = well.topsets.find_by_name('Topset1')
            top = topset.tops.find_by_name('Formation1')

            try:
                # Update the Top name and MD
                top.update_meta(name='Formation2', md=1100.0)
            except InvalidTopDataException:
                print('Invalid MD value. Must be between 0 and 100000.')
        """
        if not 0 <= md <= 100000:
            raise InvalidTopDataException

        func_data = {
            func_param: func_arg
            for func_param, func_arg in locals().items()
            if func_arg is not None and func_param != 'self'
        }
        request_data = {key: self._papi_client.prepare_papi_var(value) for key, value in func_data.items()}

        is_updated = self._papi_client.update_top_meta(top_id=self.uuid, **request_data)

        if is_updated:
            self.__dict__.update(func_data)

        return self
