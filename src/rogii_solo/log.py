from typing import Dict, List, Optional, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ComplexObject
from rogii_solo.calculations.enums import ELogMeasureUnits, EMeasureUnits
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList

WellType = Union['rogii_solo.well.Well', 'rogii_solo.well.Typewell']


class Log(ComplexObject):
    """
    Represent a :class:`Log` within a :class:`~rogii_solo.well.Well`, containing log data and related operations.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        log = well.logs.find_by_name('Log1')

        # Get the Well associated with this Log
        well = log.well
        print(well.name)

        # Get the unique identifier of the Log
        log_uuid = log.uuid
        print(log_uuid)

        # Get the name of the Log
        log_name = log.name
        print(log_name)
    """

    def __init__(self, papi_client: PapiClient, well: WellType, **kwargs):
        super().__init__(papi_client)

        self.well = well
        """:class:`~rogii_solo.well.Well` associated with this :class:`Log`."""

        self.uuid: Optional[str] = None
        """Unique identifier of this :class:`Log`."""

        self.name: Optional[str] = None
        """Name of this :class:`Log`."""

        self.__dict__.update(kwargs)

        self._points: Optional[LogPointRepository] = None

    @property
    def points(self) -> 'LogPointRepository':
        """
        Get the repository of :class:`LogPoint` associated with this :class:`Log`.

        :return: A :class:`LogPointRepository` containing the :class:`LogPoint` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            log = well.logs.find_by_name('Log1')

            # Get the LogPoint repository associated with this Log
            log_points = log.points
            print(log_points.to_dict())
        """
        if self._points is None:
            self._points = LogPointRepository(
                [
                    LogPoint(measure_units=self.well.project.measure_unit, md=point['md'], value=point['data'])
                    for point in self._papi_client.get_log_points(self.uuid)
                ]
            )

        return self._points

    def to_dict(self) -> Dict:
        """
        Convert this :class:`Log` instance to a dictionary representation.

        :return: A dictionary containing the log data of the Log.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            log = well.logs.find_by_name('Log1')

            # Convert the Log instance to a dictionary
            log_dict = log.to_dict()
            print(log_dict)
        """
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        """
        Convert this :class:`Log` instance to a pandas DataFrame representation.

        :return: A pandas DataFrame containing the log data of the Log.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            log = well.logs.find_by_name('Log1')

            # Convert the Log instance to a pandas DataFrame
            log_df = log.to_df()
            print(log_df)
        """
        return DataFrame([self.to_dict()])

    def replace_points(self, points: DataList):
        """
        Replace existing points with the provided ones.

        This method replaces points with the same MD (measured depth),
        and appends new points with MDs higher than the last existing point.
        Project units are used as index units; value_units are not sent.

        :param points: A list of points to replace the current points.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            log = well.logs.find_by_name('Log1')

            # Replace the log points data with replace values
            data = [
                {
                    "value":  0,
                    "index":  10
                },
                {
                    "value": -999.25,
                    "index": 20
                },
                {
                    "value":  3,
                    "index":  30
                }
            ]
            log.replace_points(data)

            # Update the Log metadata
            updated_log = log.update_meta(name='NewLog1')
        """
        prepared_log_points = [
            {key: self._papi_client.prepare_papi_var(value) for key, value in point.items()} for point in points
        ]
        units = ELogMeasureUnits.convert_from_measure_units(self.well.project.measure_unit)

        self._papi_client.replace_log(log_id=self.uuid, index_unit=units, log_points=prepared_log_points)
        self._points = None

    def update_meta(self, name: Optional[str] = None) -> 'Log':
        """
        Update metadata of this :class:`Log`.

        :param name: (Optional) The new name for the :class:`Log`.
        :return: Updated :class:`Log` instance.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            log = well.logs.find_by_name('Log1')

            # Update the Log metadata
            updated_log = log.update_meta(name='NewLog1')
            print(updated_log.to_dict())
        """
        func_data = {
            func_param: func_arg
            for func_param, func_arg in locals().items()
            if func_arg is not None and func_param != 'self'
        }
        request_data = {key: self._papi_client.prepare_papi_var(value) for key, value in func_data.items()}

        is_updated = self._papi_client.update_log_meta(log_id=self.uuid, **request_data)

        if is_updated:
            self.__dict__.update(func_data)

        return self


class LogPoint(BaseObject):
    """
    Represent an individual :class:`LogPoint` containing measured depth (MD) and log value.

    example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        log = well.logs.find_by_name('Log1')

        # Get the first LogPoint associated with this Log
        log_point = log.points[0]

        # Get the measure units of the LogPoint
        measure_units = log_point.measure_units
        print(measure_units)

        # Get the measured depth (MD) of the LogPoint
        md = log_point.md
        print(md)

        # Get the log value of the LogPoint
        value = log_point.value
        print(value)
    """

    def __init__(self, measure_units: EMeasureUnits, md: float, value: float):
        self.measure_units = measure_units
        """Measure units of the :class:`LogPoint`."""

        self.md: float = md
        """Measured depth (MD) of the :class:`LogPoint`."""

        self.value: float = value
        """Point value of the :class:`LogPoint`."""

    def to_dict(self, get_converted: bool = True) -> Dict:
        """
        Convert this :class:`LogPoint` instance to a dictionary representation.

        :param get_converted: (Optional) Whether to convert measure units. Default is True.
        :return: A dictionary containing the log point data of the :class:`LogPoint`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            log = well.logs.find_by_name('Log1')

            # Get the first LogPoint associated with this Log
            log_point = log.points[0]

            # Convert the LogPoint instance to a dictionary
            log_point_dict = log_point.to_dict()
            print(log_point_dict)
        """
        return {
            'md': self.safe_round(self.convert_z(value=self.md, measure_units=self.measure_units))
            if get_converted
            else self.md,
            'value': self.value,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert this :class:`LogPoint` instance to a pandas DataFrame representation.

        :param get_converted: (Optional) Whether to convert measure units. Default is True.
        :return: A pandas DataFrame containing the log point data of the :class:`LogPoint`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            log = well.logs.find_by_name('Log1')

            # Get the first LogPoint associated with this Log
            log_point = log.points[0]

            # Convert the LogPoint instance to a pandas DataFrame
            log_point_df = log_point.to_df()
            print(log_point_df)
        """
        return DataFrame([self.to_dict(get_converted)])


class LogPointRepository(list):
    """
    A repository of :class:`LogPoint` objects.

    :param objects: (Optional) List of log points to initialize the repository with.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        log = well.logs.find_by_name('Log1')

        # Get the LogPoint repository associated with this Log
        log_points = log.points
        print(log_points.to_dict())
    """

    def __init__(self, objects: List[LogPoint] = None):
        if objects is None:
            objects = []

        super().__init__(objects)

    def to_dict(self, get_converted: bool = True) -> DataList:
        """
        Convert the repository of :class:`LogPoint` objects to a list of dictionaries.

        :param get_converted: (Optional) Whether to convert measure units. Default is True.
        :return: A list of dictionaries representing the log points in the repository.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            log = well.logs.find_by_name('Log1')

            # Get the LogPoint repository associated with this Log
            log_points = log.points

            # Convert the LogPoint repository to a list of dictionaries
            log_points_dict = log_points.to_dict()
            print(log_points_dict)
        """
        return [object_.to_dict(get_converted) for object_ in self]

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the repository of :class:`LogPoint` objects to a pandas DataFrame.

        :param get_converted: (Optional) Whether to convert measure units. Default is True.
        :return: A pandas DataFrame representing the log points in the repository.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            log = well.logs.find_by_name('Log1')

            # Get the LogPoint repository associated with this Log
            log_points = log.points

            # Convert the LogPoint repository to a pandas DataFrame
            log_points_df = log_points.to_df()
            print(log_points_df)
        """
        return DataFrame(self.to_dict(get_converted))
