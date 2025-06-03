from abc import abstractmethod
from typing import Dict, List, Optional

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ComplexObject, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList
from rogii_solo.utils.objects import get_datetime


class Trace(ComplexObject):
    """
    Base class for Traces in a :class:`~rogii_solo.well.Well`.
    A trace represents a series of measurements or calculations over time or depth.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')

        # Get a time Trace name
        trace = well.time_traces.find_by_name('Trace1')
        print(trace.name)

        # Get a time Trace ID
        trace = well.time_traces.find_by_id('TraceID')
        print(trace.uuid)
    """

    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client)

        self.well: 'rogii_solo.well.Well' = well
        """The :class:`~rogii_solo.well.Well` that contains this :class:`Trace`."""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`Trace`."""

        self.name: Optional[str] = None
        """Name of the :class:`Trace`."""

        self._points: Optional[TracePointRepository] = None

        self.__dict__.update(kwargs)

    @property
    @abstractmethod
    def points(self) -> 'TracePointRepository':
        """Abstract method to get the points of the :class:`Trace`."""
        pass

    def to_dict(self) -> Dict:
        """
        Convert the :class:`Trace` instance to a dictionary.

        :return: Dictionary representation of the :class:`Trace`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            trace = well.calc_traces.find_by_name('Trace1')

            # Convert the calculated Trace to a dictionary
            trace_dict = trace.to_dict()
            print(trace_dict)
        """
        return {'uuid': self.uuid, 'name': self.uuid}

    def to_df(self) -> DataFrame:
        """
        Convert the :class:`Trace` instance to a Pandas DataFrame.

        :return: DataFrame representation of the :class:`Trace`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            trace = well.calc_traces.find_by_name('Trace1')

            # Convert the calculated Trace to a DataFrame
            trace_df = trace.to_df()
            print(trace_df)
        """
        return DataFrame([self.to_dict()])


class TimeTrace(Trace):
    """
    Represent a time-based :class:`Trace` in a :class:`~rogii_solo.well.Well`.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        time_trace = well.time_traces.find_by_name('TimeTrace1')

        # Get the hash of the time trace
        trace_hash = time_trace.hash
        print(trace_hash)

        # Get the unit of measurement
        trace_unit = time_trace.unit
        print(trace_unit)

        # Get the start and end time indices
        start_time = time_trace.start_date_time_index
        end_time = time_trace.last_date_time_index
        print(f'From {start_time} to {end_time}')
    """

    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client=papi_client, well=well, **kwargs)

        self.hash: Optional[str] = None
        """Hash value of the :class:`TimeTrace` data."""

        self.unit: Optional[str] = None
        """Unit of measurement for the :class:`TimeTrace` values."""

        self.start_date_time_index: Optional[str] = None
        """Start time of the :class:`TimeTrace` data."""

        self.last_date_time_index: Optional[str] = None
        """End time of the :class:`TimeTrace` data."""

        self.__dict__.update(kwargs)

    @property
    def points(self) -> 'TimeTracePointRepository':
        """
        Get the points associated with this :class:`TimeTrace`.

        :return: A :class:`TimeTracePointRepository` containing the :class:`TimeTrace` points.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            time_trace = well.time_traces.find_by_name('TimeTrace1')

            # Get the points of the time Trace
            points = time_trace.points
            print(points.to_dict())
        """
        if self._points is None:
            self._points = TimeTracePointRepository(
                objects=[
                    TimeTracePoint(**item)
                    for item in self._papi_client.get_well_time_trace_data(well_id=self.well.uuid, trace_id=self.uuid)
                ],
                start_date_time_index=self.start_date_time_index,
                last_date_time_index=self.last_date_time_index,
            )

        return self._points

    def to_dict(self) -> Dict:
        """
        Convert the :class:`TimeTrace` instance to a dictionary.

        :return: Dictionary representation of the :class:`TimeTrace`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            time_trace = well.time_traces.find_by_name('TimeTrace1')

            # Convert the time Trace to a dictionary
            time_trace_dict = time_trace.to_dict()
            print(time_trace_dict)
        """
        return {
            'uuid': self.uuid,
            'name': self.name,
            'hash': self.hash,
            'unit': self.unit,
            'start_date_time_index': self.start_date_time_index,
            'last_date_time_index': self.last_date_time_index,
        }


class TimeTracePoint(BaseObject):
    """
    Represent a single point in a :class:`TimeTrace`, containing a time index and value.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        time_trace = well.time_traces.find_by_name('TimeTrace1')

        # Get the first point of the time trace
        point = time_trace.points[0]

        # Get the time index of the point
        time_index = point.index
        print(time_index)

        # Get the value at this time point
        value = point.value
        print(value)
    """

    def __init__(self, **kwargs):
        self.index: Optional[str] = None
        """Time index of the measurement of this :class:`TimeTracePoint`."""

        self.value: Optional[float] = None
        """Value of the measurement of this :class:`TimeTracePoint`."""

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        """
        Convert the this :class:`TimeTracePoint` to a dictionary.

        :return: Dictionary representation of the :class:`TimeTracePoint`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            time_trace = well.time_traces.find_by_name('TimeTrace1')
            time_trace_point = time_trace.points[0]

            # Convert the time trace point to a dictionary
            time_trace_point_dict = time_trace_point.to_dict()
            print(time_trace_point_dict)
        """
        return {'index': self.index, 'value': self.value}

    def to_df(self) -> DataFrame:
        """
        Convert the this :class:`TimeTracePoint` to a Pandas DataFrame.

        :return: DataFrame representation of the this :class:`TimeTracePoint`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            time_trace = well.time_traces.find_by_name('TimeTrace1')
            time_trace_point = time_trace.points[0]

            # Convert the time trace point to a DataFrame
            time_trace_point_df = time_trace_point.to_df()
            print(time_trace_point_df)
        """
        return DataFrame([self.to_dict()])


class CalcTrace(Trace):
    """
    Represent a calculated :class:`Trace` in a :class:`~rogii_solo.well.Well`. Calculated traces contain derived
    values computed over time intervals.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        calc_trace = well.calc_traces.find_by_name('CalcTrace1')

        # Get the hash of the calculated trace
        trace_hash = calc_trace.hash
        print(trace_hash)

        # Get the start and end time indices
        start_time = calc_trace.start_date_time_index
        end_time = calc_trace.last_date_time_index
        print(f'From {start_time} to {end_time}')

        # Get available RAC codes
        rac_codes = calc_trace.rac_codes
        print(rac_codes.to_dict())
    """

    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client=papi_client, well=well, **kwargs)

        self.hash: Optional[str] = None
        """Hash value of the :class:`CalcTrace` data."""

        self.start_date_time_index: Optional[str] = None
        """Start time of the :class:`CalcTrace` data."""

        self.last_date_time_index: Optional[str] = None
        """End time of the :class:`CalcTrace` data."""

        self.__dict__.update(kwargs)

    @property
    def points(self) -> 'CalcTracePointRepository':
        """
        Get the points associated with this :class:`CalcTrace`.

        :return: A :class:`CalcTracePointRepository` containing the :class:`CalcTrace` points.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            calc_trace = well.calc_traces.find_by_name('CalcTrace1')

            # Get the points of the calculated trace
            points = calc_trace.points
            print(points.to_dict())
        """
        if self._points is None:
            self._points = CalcTracePointRepository(
                objects=[
                    CalcTracePoint(**item)
                    for item in self._papi_client.get_well_calc_trace_data(well_id=self.well.uuid, trace_id=self.uuid)
                ],
                start_date_time_index=self.start_date_time_index,
                last_date_time_index=self.last_date_time_index,
            )

        return self._points

    @property
    def rac_codes(self) -> ObjectRepository['RacCode']:
        """
        Get the RAC (Rotary Activity Code) codes associated with this :class:`CalcTrace`.

        :return: An :class:`ObjectRepository` containing :class:`RacCode` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            calc_trace = well.calc_traces.find_by_name('CalcTrace1')

            # Get the RAC codes
            rac_codes = calc_trace.rac_codes
            print(rac_codes.to_dict())
        """
        return ObjectRepository(
            objects=[
                RacCode(code=code, status=status)
                for code, status in [
                    (0, 'In Slips'),
                    (11, 'In Slips-Pump'),
                    (21, 'Drilling'),
                    (22, 'Slide Drilling'),
                    (23, 'Slide Oscilate Drilling'),
                    (31, 'Reaming'),
                    (32, 'Back Reaming'),
                    (50, 'Static'),
                    (51, 'Static-Rotate & Pump'),
                    (52, 'Static-Pump'),
                    (53, 'Static-Rotate'),
                    (54, 'Surface Operations'),
                    (61, 'Run In-Trip In'),
                    (62, 'Run In-Pump'),
                    (63, 'Run In-Rotate'),
                    (64, 'Pull Up-Pump'),
                    (65, 'Pull Up-Rotate'),
                    (66, 'Pull Up-Trip Out'),
                    (98, 'Unknown'),
                    (99, 'Missing Input'),
                ]
            ]
        )

    def to_dict(self) -> Dict:
        """
        Convert the :class:`CalcTrace` instance to a dictionary.

        :return: Dictionary representation of the :class:`CalcTrace`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            calc_trace = well.calc_traces.find_by_name('CalcTrace1')

            # Convert the calculated trace to a dictionary
            calc_trace_dict = calc_trace.to_dict()
            print(calc_trace_dict)
        """
        return {
            'uuid': self.uuid,
            'name': self.name,
            'hash': self.hash,
            'start_date_time_index': self.start_date_time_index,
            'last_date_time_index': self.last_date_time_index,
        }


class CalcTracePoint(BaseObject):
    """
    Represent a single point in a :class:`CalcTrace`, containing start time, end time, and value.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        calc_trace = well.calc_traces.find_by_name('CalcTrace1')

        # Get the first point of the calculated trace
        point = calc_trace.points[0]

        # Get the start and end times of the point
        start_time = point.start
        end_time = point.end
        print(f'From {start_time} to {end_time}')

        # Get the value for this time interval
        value = point.value
        print(value)
    """

    def __init__(self, **kwargs):
        self.start: Optional[str] = None
        """Start time of the interval."""

        self.end: Optional[str] = None
        """End time of the interval."""

        self.value: Optional[float] = None
        """Value calculated for this interval."""

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        """
        Convert the :class:`CalcTracePoint` to a dictionary.

        :return: Dictionary representation of the :class:`CalcTracePoint`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            calc_trace = well.calc_traces.find_by_name('CalcTrace1')
            calc_trace_point = calc_trace.points[0]

            # Convert the calculated trace point to a dictionary
            calc_trace_point_dict = calc_trace_point.to_dict()
            print(calc_trace_point_dict)
        """
        return {'start': self.start, 'end': self.end, 'value': self.value}

    def to_df(self) -> DataFrame:
        """
        Convert the :class:`CalcTracePoint` to a Pandas DataFrame.

        :return: DataFrame representation of the :class:`CalcTracePoint`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            calc_trace = well.calc_traces.find_by_name('CalcTrace1')
            calc_trace_point = calc_trace.points[0]

            # Convert the calculated trace point to a DataFrame
            calc_trace_point_df = calc_trace_point.to_df()
            print(calc_trace_point_df)
        """
        return DataFrame([self.to_dict()])


class RacCode(BaseObject):
    """
    Represent a RAC (Rotary Activity Code) code and its associated status.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        calc_trace = well.calc_traces.find_by_name('CalcTrace1')

        # Get all RAC codes
        rac_codes = calc_trace.rac_codes

        # Get a specific RAC code
        drilling_code = rac_codes.find_by_code(21)
        print(f'Code {drilling_code.code}: {drilling_code.status}')
    """

    def __init__(self, **kwargs):
        self.code: Optional[str] = None
        """Numeric code of the :class:`RacCode`."""

        self.status: Optional[str] = None
        """Description of the :class:`RacCode`."""

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        """
        Convert the :class:`RacCode` to a dictionary.

        :return: Dictionary representation of the :class:`RacCode`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            calc_trace = well.calc_traces.find_by_name('CalcTrace1')
            rac_code = calc_trace.rac_codes[0]

            # Convert the RAC code to a dictionary
            rac_code_dict = rac_code.to_dict()
            print(rac_code_dict)
        """
        return {'code': self.code, 'status': self.status}

    def to_df(self) -> DataFrame:
        """
        Convert the :class:`RacCode` to a Pandas DataFrame.

        :return: DataFrame representation of the :class:`RacCode`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            calc_trace = well.calc_traces.find_by_name('CalcTrace1')
            rac_code = calc_trace.rac_codes[0]

            # Convert the RAC code to a DataFrame
            rac_code_df = rac_code.to_df()
            print(rac_code_df)
        """
        return DataFrame([self.to_dict()])


class TracePointRepository(list):
    """
    Base class for repositories of trace points. Provides common functionality for
    managing collections of trace points.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        time_trace = well.time_traces.find_by_name('TimeTrace1')

        # Get instance of the TracePointRepository
        points = time_trace.points

        # Get start date time index of the points
        start_index = points.start_date_time_index
        print(start_index)

        # Get last date time index of the points
        last_index = points.last_date_time_index
        print(last_index)
    """

    def __init__(
        self,
        start_date_time_index: str,
        last_date_time_index: str,
        objects: List[TimeTracePoint | CalcTracePoint] = None,
    ):
        if objects is None:
            objects = []

        super().__init__(objects)

        self.start_date_time_index: str = start_date_time_index
        """Start time of the trace data."""

        self.last_date_time_index: str = last_date_time_index
        """End time of the trace data."""

    @abstractmethod
    def to_dict(self, time_from: str = None, time_to: str = None) -> DataList:
        pass

    def to_df(self, time_from: str = None, time_to: str = None) -> DataFrame:
        """
        Convert the :class:`TracePointRepository` to a Pandas DataFrame.

        :param time_from: (Optional) Start time for filtering points
        :param time_to: (Optional) End time for filtering points
        :return: DataFrame representation of the filtered points

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            calc_trace = well.calc_traces.find_by_name('CalcTrace1')
            points = calc_trace.points

            # Convert the points to a DataFrame
            points_df = points.to_df(time_from='2023-01-01T00:00:00', time_to='2023-01-02T00:00:00')
            print(points_df)
        """
        return DataFrame(self.to_dict(time_from=time_from, time_to=time_to))


class TimeTracePointRepository(TracePointRepository):
    """
    Repository for :class:`TimeTracePoint` objects with time-based filtering capabilities.
    """

    def to_dict(self, time_from: str = None, time_to: str = None):
        """
        Converts the :class:`TimeTracePointRepository` to a list of dictionaries, filtered by time range.

        :param time_from: (Optional) Start time for filtering points
        :param time_to: (Optional) End time for filtering points
        :return: List of dictionaries representing the filtered points

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            time_trace = well.time_traces.find_by_name('TimeTrace1')

            # Get all points
            points = time_trace.points

            # Get points within a specific time range
            filtered_points = points.to_dict(time_from='2023-01-01T00:00:00', time_to='2023-01-02T00:00:00')
            print(filtered_points)
        """
        time_from_dt = get_datetime(time_from if time_from else self.start_date_time_index)
        time_to_dt = get_datetime(time_to if time_to else self.last_date_time_index)

        return [point.to_dict() for point in self if time_from_dt <= get_datetime(point.index) <= time_to_dt]


class CalcTracePointRepository(TracePointRepository):
    """
    Repository for :class:`CalcTracePoint` objects with time-based filtering capabilities.
    """

    def to_dict(self, time_from: str = None, time_to: str = None):
        """
        Convert the :class:`CalcTracePointRepository` to a list of dictionaries, filtered by time range.
        Points that overlap with the specified time range are included.

        :param time_from: (Optional) Start time for filtering points
        :param time_to: (Optional) End time for filtering points
        :return: List of dictionaries representing the filtered points

        :example:


        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            calc_trace = well.calc_traces.find_by_name('CalcTrace1')

            # Get all points
            points = calc_trace.points

            # Get points within a specific time range
            filtered_points = points.to_dict(time_from='2023-01-01T00:00:00', time_to='2023-01-02T00:00:00')
            print(filtered_points)
        """
        time_from_dt = max(
            get_datetime(time_from or self.start_date_time_index),
            get_datetime(self.start_date_time_index),
        )
        time_to_dt = min(get_datetime(time_to or self.last_date_time_index), get_datetime(self.last_date_time_index))

        points_data = []

        for point in self:
            point_start_dt = get_datetime(point.start)
            point_end_dt = get_datetime(point.end)

            if (
                (point_start_dt >= time_from_dt and point_end_dt <= time_to_dt)
                or (time_from_dt < point_end_dt <= time_to_dt)
                or (time_from_dt <= point_start_dt < time_to_dt)
            ):
                points_data.append(point.to_dict())

        return points_data
