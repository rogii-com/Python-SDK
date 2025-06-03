from typing import Dict, Optional, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ComplexObject, ObjectRepository
from rogii_solo.log import LogPoint, LogPointRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList

WellType = Union['rogii_solo.well.Well', 'rogii_solo.well.Typewell']


class Mudlog(ComplexObject):
    """
    Represent a :class:`Mudlog` within a :class:`~rogii_solo.well.Well`, containing lithology data and operations.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        projects = solo_client.set_project_by_name('Project1')
        well = projects.wells.find_by_name('Well1')
        mudlog = well.mudlogs.find_by_name('Mudlog1')

        # Get the Well associated with this Mudlog
        well = mudlog.well
        print(well.name)

        # Get the unique identifier of the Mudlog
        mudlog_uuid = mudlog.uuid
        print(mudlog_uuid)

        # Get the name of the Mudlog
        mudlog_name = mudlog.name
        print(mudlog_name)
    """

    def __init__(self, papi_client: PapiClient, well: WellType, **kwargs):
        super().__init__(papi_client)

        self.well = well
        """:class:`~rogii_solo.well.Well` associated with this :class:`Mudlog`."""

        self.uuid: Optional[str] = None
        """Unique identifier of this :class:`Mudlog`."""

        self.name: Optional[str] = None
        """Name of this :class:`Mudlog`."""

        self.__dict__.update(kwargs)

        self._logs: Optional['LithologyLogRepository'] = None

    @property
    def logs(self) -> 'LithologyLogRepository':
        """
        Get the repository of :class:`LithologyLog` associated with this :class:`Mudlog`.

        :return: A :class:`LithologyLogRepository` containing the :class:`LithologyLog` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            mudlog = well.mudlogs.find_by_name('Mudlog1')

            # Get the LithologyLog repository associated with this Mudlog
            lithology_logs = mudlog.logs
            print(lithology_logs.to_dict())
        """
        if self._logs is None:
            self._logs = LithologyLogRepository(
                [
                    LithologyLog(mudlog=self, _points_data=item['log_points'], **item)
                    for item in self._papi_client.get_mudlog_data(self.uuid)
                ]
            )

        return self._logs

    def to_dict(self) -> Dict:
        """
        Convert this :class:`Mudlog` instance to a dictionary representation.

        :return: A dictionary containing the :class:`Mudlog` data.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            mudlog = well.mudlogs.find_by_name('Mudlog1')

            # Convert the Mudlog instance to a dictionary
            mudlog_dict = mudlog.to_dict()
            print(mudlog_dict)
        """
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        """
        Convert this :class:`Mudlog` instance to a pandas DataFrame representation.

        :return: A pandas DataFrame containing the :class:`Mudlog` data.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            mudlog = well.mudlogs.find_by_name('Mudlog1')

            # Convert the Mudlog instance to a pandas DataFrame
            mudlog_df = mudlog.to_df()
            print(mudlog_df)
        """
        return DataFrame([self.to_dict()])


class LithologyLog(BaseObject):
    """
    Represent a :class:`LithologyLog` within a :class:`Mudlog`, containing lithology data for a specific property.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        projects = solo_client.set_project_by_name('Project1')
        well = projects.wells.find_by_name('Well1')
        mudlog = well.mudlogs.find_by_name('Mudlog1')

        # Get the first LithologyLog associated with this Mudlog
        litho_log = mudlog.logs[0]

        # Get the Mudlog associated with this LithologyLog
        parent_mudlog = litho_log.mudlog
        print(parent_mudlog.name)

        # Get the unique identifier of the LithologyLog
        litho_log_uuid = litho_log.uuid
        print(litho_log_uuid)

        # Get the name of the LithologyLog
        litho_log_name = litho_log.name
        print(litho_log_name)
    """

    def __init__(self, mudlog: Mudlog, **kwargs):
        self.mudlog = mudlog
        """:class:`Mudlog` associated with this :class:`LithologyLog`."""

        self.uuid: Optional[str] = None
        """Unique identifier of this :class:`LithologyLog`."""

        self.name: Optional[str] = None
        """Name of this :class:`LithologyLog`."""

        self._points: Optional[LogPointRepository] = None
        self._points_data: Optional[DataList] = None

        self.__dict__.update(kwargs)

    @property
    def points(self) -> 'LogPointRepository':
        """
        Get the repository of :class:`LogPoint` associated with this :class:`LithologyLog`.

        :return: A :class:`LogPointRepository` containing the :class:`LogPoint` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            mudlog = well.mudlogs.find_by_name('Mudlog1')

            # Get the first LithologyLog associated with this Mudlog
            litho_log = mudlog.logs[0]

            # Get the LogPoint repository associated with this LithologyLog
            log_points = litho_log.points
            print(log_points.to_dict())
        """
        if self._points is None:
            self._points = LogPointRepository(
                [
                    LogPoint(measure_units=self.mudlog.well.project.measure_unit, md=point['md'], value=point['data'])
                    for point in self._points_data
                ]
            )

        return self._points

    def to_dict(self) -> Dict:
        """
        Convert this :class:`LithologyLog` instance to a dictionary representation.

        :return: A dictionary containing the :class:`LithologyLog` data.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            mudlog = well.mudlogs.find_by_name('Mudlog1')

            # Get the first LithologyLog associated with this Mudlog
            litho_log = mudlog.logs[0]

            # Convert the LithologyLog instance to a dictionary
            litho_log_dict = litho_log.to_dict()
            print(litho_log_dict)
        """
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        """
        Convert this :class:`LithologyLog` instance to a pandas DataFrame representation.

        :return: A pandas DataFrame containing the lithology log data.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            mudlog = well.mudlogs.find_by_name('Mudlog1')

            # Get the first LithologyLog associated with this Mudlog
            litho_log = mudlog.logs[0]

            # Convert the LithologyLog instance to a pandas DataFrame
            litho_log_df = litho_log.to_df()
            print(litho_log_df)
        """
        return DataFrame([self.to_dict()])


class LithologyLogRepository(ObjectRepository):
    """
    A repository of :class:`LithologyLog` objects.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        projects = solo_client.set_project_by_name('Project1')
        well = projects.wells.find_by_name('Well1')
        mudlog = well.mudlogs.find_by_name('Mudlog1')

        # Get the LithologyLog repository associated with this Mudlog
        lithology_logs = mudlog.logs
        print(lithology_logs.to_dict())
    """

    def to_dict(self) -> DataList:
        """
        Convert the repository of :class:`LithologyLog` objects to a list of dictionaries.

        :return: A list of dictionaries containing the :class:`LithologyLog` data.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            mudlog = well.mudlogs.find_by_name('Mudlog1')

            # Convert the LithologyLog repository to a list of dictionaries
            lithology_logs = mudlog.logs
            print(lithology_logs.to_dict())
        """
        pass

    def to_df(self) -> DataFrame:
        """
        Convert the repository of :class:`LithologyLog` objects to a pandas DataFrame.

        This method creates a DataFrame with all lithology logs merged by MD (Measured Depth).

        :return: A pandas DataFrame representing all lithology logs merged by MD.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            mudlog = well.mudlogs.find_by_name('Mudlog1')

            # Convert all lithology logs to a combined DataFrame
            lithology_df = mudlog.logs.to_df()
            print(lithology_df)
        """
        mudlog_df = DataFrame(columns=('MD',))

        for log in self:
            log_df = log.points.to_df().rename(columns={'md': 'MD', 'value': log.name})
            mudlog_df = mudlog_df.merge(right=log_df, on='MD', how='outer')

        return mudlog_df
