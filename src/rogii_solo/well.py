from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.project
from rogii_solo.base import BaseObject, ComplexObject, ObjectRepository
from rogii_solo.calculations.converters import feet_to_meters
from rogii_solo.calculations.enums import ELogMeasureUnits
from rogii_solo.comment import Comment
from rogii_solo.interpretation import Interpretation
from rogii_solo.log import Log
from rogii_solo.mudlog import Mudlog
from rogii_solo.papi.client import PapiClient
from rogii_solo.target_line import TargetLine
from rogii_solo.topset import Topset
from rogii_solo.trace import CalcTrace, TimeTrace
from rogii_solo.trajectory import TrajectoryPoint, TrajectoryPointRepository
from rogii_solo.types import DataList
from rogii_solo.utils.objects import find_by_uuid

keep_value = object()


class Well(ComplexObject):
    """
    Represent a :class:`Well` in a :class:`~rogii_solo.project.Project`. Contains all well-related data and operations
    including :class:`~rogii_solo.trajectory.Trajectory`, :class:`~rogii_solo.log.Log`,
    :class:`~rogii_solo.interpretation.Interpretation`, :class:`~rogii_solo.trace.CalcTrace`,
    :class:`~rogii_solo.trace.TimeTrace`, :class:`~rogii_solo.comment.Comment` and so on.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')

        # Get a Well by name
        well = project.wells.find_by_name('Well1')

        # Get the Project this Well belongs to
        project = well.project
        print(project.name)

        # Get Well attributes
        print(f"Well name: {well.name}")
        print(f"Well API: {well.api}")
        print(f"Well operator: {well.operator}")
        print(f"Well KB: {well.kb}")
        print(f"Well surface coordinates: ({well.xsrf}, {well.ysrf})")
        print(f"Well real coordinates: ({well.xsrf_real}, {well.ysrf_real})")
        print(f"Well azimuth: {well.azimuth}")
        print(f"Well convergence: {well.convergence}")
        print(f"Well tie-in TVD: {well.tie_in_tvd}")
        print(f"Well tie-in NS: {well.tie_in_ns}")
        print(f"Well tie-in EW: {well.tie_in_ew}")
        print(f"Well starred: {well.starred}")
    """

    def __init__(self, papi_client: PapiClient, project: 'rogii_solo.project.Project', **kwargs):
        super().__init__(papi_client)

        self.project = project
        """The :class:`~rogii_solo.project.Project` this :class:`Well` belongs to."""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`Well`."""

        self.name: Optional[str] = None
        """Name of the :class:`Well`."""

        self.xsrf: Optional[float] = None
        """Surface X coordinate of the :class:`Well`."""

        self.ysrf: Optional[float] = None
        """Surface Y coordinate of the :class:`Well`."""

        self.xsrf_real: Optional[float] = None
        """Real surface X coordinate of the :class:`Well`."""

        self.ysrf_real: Optional[float] = None
        """Real surface Y coordinate of the :class:`Well`."""

        self.kb: Optional[float] = None
        """Kelly Bushing (KB) elevation of the :class:`Well`."""

        self.api: Optional[str] = None
        """API number of the :class:`Well`."""

        self.operator: Optional[str] = None
        """Operator of the :class:`Well`."""

        self.azimuth: Optional[float] = None
        """Azimuth angle of the :class:`Well` in degrees."""

        self.convergence: Optional[float] = None
        """Grid convergence angle of the :class:`Well` in degrees."""

        self.tie_in_tvd: Optional[float] = None
        """True Vertical Depth (TVD) at the tie-in point."""

        self.tie_in_ns: Optional[float] = None
        """North-South coordinate at the tie-in point."""

        self.tie_in_ew: Optional[float] = None
        """East-West coordinate at the tie-in point."""

        self.starred: Optional[bool] = None
        """Whether this :class:`Well` is starred."""

        self.__dict__.update(kwargs)

        self.kb = 0 if self.kb is None else self.kb
        self.tie_in_ns = 0 if self.tie_in_ns is None else self.tie_in_ns
        self.tie_in_ew = 0 if self.tie_in_ew is None else self.tie_in_ew

        self._trajectory: Optional[TrajectoryPointRepository[TrajectoryPoint]] = None
        self._interpretations: Optional[ObjectRepository[Interpretation]] = None
        self._starred_interpretation: Optional[Interpretation] = None
        self._target_lines: Optional[ObjectRepository[TargetLine]] = None
        self._starred_target_line: Optional[TargetLine] = None
        self._nested_wells: Optional[ObjectRepository[NestedWell]] = None
        self._starred_nested_well: Optional[NestedWell] = None
        self._logs: Optional[ObjectRepository[Log]] = None
        self._topsets: Optional[ObjectRepository[Topset]] = None
        self._starred_topset: Optional[Topset] = None
        self._mudlogs: Optional[ObjectRepository[Mudlog]] = None
        self._time_traces: Optional[ObjectRepository[TimeTrace]] = None
        self._calc_traces: Optional[ObjectRepository[CalcTrace]] = None
        self._linked_typewells: Optional[ObjectRepository[Typewell]] = None
        self._comments: Optional[DataList] = None
        self._attributes: Optional[Dict] = None

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        """
        Get the trajectory data for this :class:`Well`.

        :return: A :class:`TrajectoryPointRepository` containing the Well's trajectory points.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get the Well's trajectory
            trajectory = well.trajectory
            print(trajectory.to_dict())
        """
        if self._trajectory is None:
            self._trajectory = TrajectoryPointRepository(
                objects=[
                    TrajectoryPoint(measure_units=self.project.measure_unit, **item)
                    for item in self._papi_client.get_well_trajectory_data(well_id=self.uuid)
                ]
            )

        return self._trajectory

    @property
    def interpretations(self) -> ObjectRepository[Interpretation]:
        """
        Get the :class:`~rogii_solo.base.ObjectRepository` of :class:`~rogii_solo.interpretation.Interpretation`
        instances associated with this :class:`Well`.

        :return: An :class:`~rogii_solo.base.ObjectRepository`
        containing :class:`~rogii_solo.interpretation.Interpretation` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all interpretations
            interpretations = well.interpretations
            print(interpretations.to_dict())

            # Find a specific interpretation
            interpretation = interpretations.find_by_name('Interpretation1')
            print(interpretation.to_dict())
        """
        if self._interpretations is None:
            self._interpretations = ObjectRepository(
                objects=[
                    Interpretation(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_well_interpretations_data(well_id=self.uuid)
                ]
            )

        return self._interpretations

    @property
    def starred_interpretation(self) -> Optional[Interpretation]:
        """
        Get the starred :class:`~rogii_solo.interpretation.Interpretation` for this :class:`Well`.

        :return: The starred :class:`~rogii_solo.interpretation.Interpretation` instance, or None if none is starred.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get the starred interpretation
            starred = well.starred_interpretation

            if starred:
                print(starred.to_dict())
        """
        if self._starred_interpretation is None:
            starred_interpretation_id = self._find_by_path(obj=self.starred, path='interpretation')
            self._starred_interpretation = self.interpretations.find_by_id(starred_interpretation_id)

        return self._starred_interpretation

    @property
    def target_lines(self) -> ObjectRepository[TargetLine]:
        """
        Get the :class:`~rogii_solo.target_line.TargetLine` associated with this :class:`Well`.

        :return: An :class:`ObjectRepository` containing :class:`~rogii_solo.target_line.TargetLine` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all target lines
            target_lines = well.target_lines
            print(target_lines.to_dict())

            # Find a specific target line
            target_line = target_lines.find_by_name('TargetLine1')
            print(target_line.to_dict())
        """
        if self._target_lines is None:
            self._target_lines = ObjectRepository(
                objects=[TargetLine(**item) for item in self._papi_client.get_well_target_lines_data(well_id=self.uuid)]
            )

        return self._target_lines

    @property
    def starred_target_line(self) -> Optional[TargetLine]:
        """
        Get the starred :class:`~rogii_solo.target_line.TargetLine` for this :class:`Well`.

        :return: The starred :class:`~rogii_solo.target_line.TargetLine` instance, or None if none is starred.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get the starred target line
            starred = well.starred_target_line
            if starred:
                print(starred.to_dict())
        """
        if self._starred_target_line is None:
            starred_target_line_id = self._find_by_path(obj=self.starred, path='target_line')
            self._starred_target_line = self.target_lines.find_by_id(starred_target_line_id)

        return self._starred_target_line

    @property
    def nested_wells(self) -> ObjectRepository['NestedWell']:
        """
        Get the :class:`NestedWell`, representing well, plan associated with this :class:`Well`.

        :return: An :class:`ObjectRepository` containing :class:`NestedWell` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all well plans
            well_plans = well.nested_wells
            print(well_plans.to_dict())

            # Find a specific well plan
            well_plan = well_plans.find_by_name('WellPlan1')
            print(well_plan.to_dict())
        """
        if self._nested_wells is None:
            self._nested_wells = ObjectRepository(
                objects=[
                    NestedWell(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_well_nested_wells_data(well_id=self.uuid)
                ]
            )

        return self._nested_wells

    @property
    def linked_typewells(self) -> ObjectRepository['Typewell']:
        """
        Get the linked :class:`~rogii_solo.well.Typewell` associated with this :class:`Well`.

        :return: An :class:`ObjectRepository` containing :class:`~rogii_solo.well.Typewell` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all linked type wells
            type_wells = well.linked_typewells
            print(type_wells.to_dict())

            # Find a specific type well
            type_well = type_wells.find_by_name('TypeWell1')
            print(type_well.to_dict())
        """
        if self._linked_typewells is None:
            self._linked_typewells = ObjectRepository(
                objects=[
                    Typewell(papi_client=self._papi_client, project=self.project, **item)
                    for item in self._get_linked_typewells_data()
                ]
            )

        return self._linked_typewells

    @property
    def starred_nested_well(self) -> Optional['NestedWell']:
        """
        Get the starred :class:`NestedWell` for this :class:`Well`.

        :return: The starred :class:`NestedWell` instance, or None if none is starred.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get the starred well plan
            starred_well_plan = well.starred_nested_well

            if starred_well_plan:
                print(starred_well_plan.to_dict())
        """
        if self._starred_nested_well is None:
            starred_nested_well_id = self._find_by_path(obj=self.starred, path='nested_well')
            self._starred_nested_well = self.nested_wells.find_by_id(starred_nested_well_id)

        return self._starred_nested_well

    @property
    def logs(self) -> ObjectRepository[Log]:
        """
        Get the :class:`~rogii_solo.log.Log` associated with this :class:`Well`.

        :return: An :class:`~rogii_solo.base.ObjectRepository` containing :class:`~rogii_solo.log.Log` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all logs
            logs = well.logs
            print(logs.to_dict())

            # Find a specific log
            log = logs.find_by_name('Log1')
            print(log.to_dict())
        """
        if self._logs is None:
            self._logs = ObjectRepository(
                objects=[
                    Log(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_well_logs_data(well_id=self.uuid)
                ]
            )

        return self._logs

    @property
    def topsets(self) -> ObjectRepository[Topset]:
        """
        Get the :class:`~rogii_solo.topset.Topset` associated with this :class:`Well`.

        :return: An :class:`~rogii_solo.base.ObjectRepository` containing :class:`~rogii_solo.topset.Topset` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all topsets
            topsets = well.topsets
            print(topsets.to_dict())

            # Find a specific topset
            topset = topsets.find_by_name('Topset1')
            print(topset.to_dict())
        """
        if self._topsets is None:
            self._topsets = ObjectRepository(
                objects=[
                    Topset(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_well_topsets_data(well_id=self.uuid)
                ]
            )

        return self._topsets

    @property
    def starred_topset(self) -> Optional[Topset]:
        """
        Get the starred :class:`~rogii_solo.topset.Topset` for this :class:`Well`.

        :return: The starred :class:`~rogii_solo.topset.Topset` instance, or None if none is starred.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get the starred topset
            starred = well.starred_topset

            if starred:
                print(starred.to_dict())
        """
        if self._starred_topset is None:
            starred_topset_id = self._find_by_path(obj=self.starred, path='topset')
            self._starred_topset = self.topsets.find_by_id(starred_topset_id)

        return self._starred_topset

    @property
    def mudlogs(self) -> ObjectRepository[Mudlog]:
        """
        Get the :class:`~rogii_solo.mudlog.Mudlog` associated with this :class:`Well`.

        :return: An :class:`~rogii_solo.base.ObjectRepository` containing :class:`~rogii_solo.mudlog.Mudlog` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all mudlogs
            mudlogs = well.mudlogs
            print(mudlogs.to_dict())

            # Find a specific mudlog
            mudlog = mudlogs.find_by_name('Mudlog1')
            print(mudlog.to_dict())
        """
        if self._mudlogs is None:
            self._mudlogs = ObjectRepository(
                objects=[
                    Mudlog(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_well_mudlogs_data(well_id=self.uuid)
                ]
            )

        return self._mudlogs

    @property
    def time_traces(self) -> ObjectRepository[TimeTrace]:
        """
        Get the :class:`~rogii_solo.trace.TimeTrace` associated with this :class:`Well`.

        :return: An :class:`ObjectRepository` containing :class:`~rogii_solo.trace.TimeTrace` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all time traces
            time_traces = well.time_traces
            print(time_traces.to_dict())

            # Find a specific time trace
            time_trace = time_traces.find_by_name('TimeTrace1')
            print(time_trace.to_dict())
        """
        if self._time_traces is None:
            self._time_traces = ObjectRepository(
                objects=[
                    TimeTrace(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_well_mapped_time_traces_data(self.uuid)
                ]
            )

        return self._time_traces

    @property
    def calc_traces(self) -> ObjectRepository[CalcTrace]:
        """
        Get the :class:`~rogii_solo.trace.CalcTrace` associated with this :class:`Well`.

        :return: An :class:`ObjectRepository` containing :class:`~rogii_solo.trace.CalcTrace` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all calculated traces
            calc_traces = well.calc_traces
            print(calc_traces.to_dict())

            # Find a specific calculated trace
            calc_trace = calc_traces.find_by_name('CalcTrace1')
            print(calc_trace.to_dict())
        """
        if self._calc_traces is None:
            self._calc_traces = ObjectRepository(
                objects=[
                    CalcTrace(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_well_mapped_calc_traces_data(self.uuid)
                ]
            )

        return self._calc_traces

    @property
    def comments(self) -> ObjectRepository[Comment]:
        """
        Get the :class:`~rogii_solo.comment.Comment` associated with this :class:`Well`.

        :return: An :class:`ObjectRepository` containing :class:`~rogii_solo.comment.Comment` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get all comments
            comments = well.comments
            print(comments.to_dict())

            # Find a specific comment
            comment = comments.find_by_name('Comment1')
            print(comment.to_dict())
        """
        if self._comments is None:
            self._comments = ObjectRepository(
                objects=[
                    Comment(
                        well=self,
                        comment_id=item['comment_id'],
                        name=item['name'],
                        _comment_boxes_data=item['comment_boxes'],
                    )
                    for item in self._papi_client.get_well_comments_data(well_id=self.uuid)
                ]
            )

        return self._comments

    @property
    def attributes(self) -> 'WellAttributes':
        """
        Get the attributes associated with this :class:`Well`.

        :return: A :class:`WellAttributes` instance containing the well's attributes.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get well attributes
            attributes = well.attributes
            print(attributes.to_dict())
        """
        if self._attributes is None:
            self._attributes = WellAttributes(well=self, **self._get_attributes_data())

        return self._attributes

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`Well` instance to a dictionary.

        :param get_converted: Whether to convert values to project units
        :return: Dictionary representation of the :class:`Well`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Convert the Well to a dictionary with unit conversion
            well_dict = well.to_dict()
            print(well_dict)

            # Convert the Well to a dictionary without unit conversion
            raw_dict = well.to_dict(get_converted=False)
            print(raw_dict)
        """
        measure_units = self.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'api': self.api,
            'operator': self.operator,
            'xsrf': (
                self.safe_round(self.convert_xy(value=self.xsrf, measure_units=measure_units, force_to_meters=True))
                if get_converted
                else self.xsrf
            ),
            'ysrf': (
                self.safe_round(self.convert_xy(value=self.ysrf, measure_units=measure_units, force_to_meters=True))
                if get_converted
                else self.ysrf
            ),
            'xsrf_real': self.safe_round(self.xsrf_real) if get_converted else feet_to_meters(self.xsrf_real),
            'ysrf_real': self.safe_round(self.ysrf_real) if get_converted else feet_to_meters(self.ysrf_real),
            'kb': (
                self.safe_round(self.convert_z(value=self.kb, measure_units=measure_units))
                if get_converted
                else self.kb
            ),
            'azimuth': self.safe_round(self.convert_angle(self.azimuth)) if get_converted else self.azimuth,
            'convergence': self.safe_round(self.convert_angle(self.convergence)) if get_converted else self.convergence,
            'tie_in_tvd': (
                self.safe_round(self.convert_z(value=self.tie_in_tvd, measure_units=measure_units))
                if get_converted
                else self.tie_in_tvd
            ),
            'tie_in_ns': (
                self.safe_round(self.convert_xy(value=self.tie_in_ns, measure_units=measure_units))
                if get_converted
                else self.tie_in_ns
            ),
            'tie_in_ew': (
                self.safe_round(self.convert_xy(value=self.tie_in_ew, measure_units=measure_units))
                if get_converted
                else self.tie_in_ew
            ),
            'starred': self.starred,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`Well` instance to a Pandas DataFrame.

        :param get_converted: Whether to convert values to project units
        :return: DataFrame representation of the :class:`Well`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Convert the Well to a DataFrame
            well_df = well.to_df()
            print(well_df)
        """
        return DataFrame([self.to_dict(get_converted)])

    def replace_trajectory(self, md_uom: str, incl_uom: str, azi_uom: str, trajectory_stations: DataList):
        """
        Replace the trajectory data for this :class:`Well`.

        :param md_uom: Unit of measurement for measured depth values
        :param incl_uom: Unit of measurement for inclination values
        :param azi_uom: Unit of measurement for azimuth values
        :param trajectory_stations: List of trajectory points data

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Replace the Well's trajectory
            trajectory_data = [
                {'md': 0, 'incl': 0, 'azim': 0},
                {'md': 1000, 'incl': 45, 'azim': 180},
            ]
            well.replace_trajectory(
                md_uom='ft',
                incl_uom='deg',
                azi_uom='deg',
                trajectory_stations=trajectory_data
            )
        """
        prepared_trajectory_stations = [
            {key: self._papi_client.prepare_papi_var(value) for key, value in point.items()}
            for point in trajectory_stations
        ]

        self._papi_client.replace_well_trajectory(
            well_id=self.uuid,
            md_uom=md_uom,
            incl_uom=incl_uom,
            azi_uom=azi_uom,
            trajectory_stations=prepared_trajectory_stations,
        )
        self._trajectory = None

    def _get_linked_typewells_data(self) -> DataList:
        linked_typewells_data = []
        well_typewells_data = self._papi_client.get_well_linked_typewells_data(well_id=self.uuid)

        for linked_typewell_data in well_typewells_data:
            typewell_data = self._papi_client.get_typewell_data(typewell_id=linked_typewell_data['typewell_id'])
            shift = linked_typewell_data.get('shift')

            if shift is not None:
                linked_typewells_data.append({**typewell_data, 'shift': shift})

        return linked_typewells_data

    def _get_attributes_data(self) -> Dict:
        return {
            attribute_name: attribute['value']
            for attribute_name, attribute in self._papi_client.get_well_attributes(well_id=self.uuid).items()
        }

    def create_nested_well(
        self,
        name: str,
        operator: str,
        api: str,
        xsrf: float,
        ysrf: float,
        kb: float,
        tie_in_tvd: float,
        tie_in_ns: float,
        tie_in_ew: float,
    ):
        """
        Create a new :class:`NestedWell` in this :class:`Well`.

        :param name: Name of the :class:`NestedWell`
        :param operator: Operator of the :class:`NestedWell`
        :param api: API number of the :class:`NestedWell`
        :param xsrf: Surface X coordinate of the :class:`NestedWell`
        :param ysrf: Surface Y coordinate of the :class:`NestedWell`
        :param kb: Kelly Bushing (KB) elevation of the :class:`NestedWell`
        :param tie_in_tvd: True Vertical Depth (TVD) at the tie-in point
        :param tie_in_ns: North-South coordinate at the tie-in point
        :param tie_in_ew: East-West coordinate at the tie-in point

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Create a new well plan
            well.create_nested_well(
                name='WellPlan1',
                operator='Operator1',
                api='API123',
                xsrf=1000.0,
                ysrf=2000.0,
                kb=100.0,
                tie_in_tvd=500.0,
                tie_in_ns=300.0,
                tie_in_ew=400.0
            )
        """
        nested_well_id = self._papi_client.create_well_nested_well(
            well_id=self.uuid,
            name=name,
            operator=operator,
            api=api,
            xsrf=self._papi_client.prepare_papi_var(xsrf),
            ysrf=self._papi_client.prepare_papi_var(ysrf),
            kb=self._papi_client.prepare_papi_var(kb),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew),
        )

        # No raw method for nested well
        nested_well_data = find_by_uuid(
            value=nested_well_id['uuid'],
            input_list=self._papi_client.get_well_nested_wells_data(well_id=self.uuid, query=name),
        )

        if self._nested_wells is not None:
            self._nested_wells.append(NestedWell(papi_client=self._papi_client, well=self, **nested_well_data))

    def create_topset(self, name: str):
        """
        Create a new :class:`~rogii_solo.topset.Topset` in this :class:`Well`.

        :param name: Name of the :class:`~rogii_solo.topset.Topset`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Create a new topset
            well.create_topset('Topset1')
        """
        topset_id = self._papi_client.create_well_topset(well_id=self.uuid, name=name)

        if self._topsets is not None:
            self._topsets.append(Topset(papi_client=self._papi_client, well=self, uuid=topset_id, name=name))

    def create_log(self, name: str, points: DataList):
        """
        Create a new :class:`~rogii_solo.log.Log` in this :class:`Well`.

        :param name: Name of the :class:`~rogii_solo.log.Log`
        :param points: List of :class:`~rogii_solo.log.Log` points data

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Create a new log with some points
            points = [
                {'md': 0, 'value': 100},
                {'md': 100, 'value': 200},
                {'md': 200, 'value': 300}
            ]
            well.create_log(name='Log1', points=points)
        """
        log_id = self._papi_client.create_well_log(well_id=self.uuid, name=name)
        prepared_points = [
            {key: self._papi_client.prepare_papi_var(value) for key, value in point.items()} for point in points
        ]
        units = ELogMeasureUnits.convert_from_measure_units(self.project.measure_unit)

        self._papi_client.replace_log(log_id=log_id['uuid'], index_unit=units, log_points=prepared_points)

        if self._logs is not None:
            self._logs.append(
                Log(
                    papi_client=self._papi_client,
                    well=self,
                    uuid=log_id['uuid'],
                    name=name,
                )
            )

    def create_target_line(
        self,
        name: str,
        origin_x: float,
        origin_y: float,
        origin_z: float,
        target_x: float,
        target_y: float,
        target_z: float,
    ):
        """
        Create a new :class:`~rogii_solo.target_line.TargetLine` in this :class:`Well`.

        :param name: Name of the :class:`~rogii_solo.target_line.TargetLine`
        :param origin_x: X coordinate of the origin point
        :param origin_y: Y coordinate of the origin point
        :param origin_z: Z coordinate (TVDSS) of the origin point
        :param target_x: X coordinate of the target point
        :param target_y: Y coordinate of the target point
        :param target_z: Z coordinate (TVDSS) of the target point

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Create a new target line
            well.create_target_line(
                name='TargetLine1',
                origin_x=1000.0,
                origin_y=2000.0,
                origin_z=100.0,
                target_x=1500.0,
                target_y=2500.0,
                target_z=200.0
            )
        """
        target_line_id = self._papi_client.create_well_target_line(
            well_id=self.uuid,
            name=name,
            origin_x=self._papi_client.prepare_papi_var(origin_x),
            origin_y=self._papi_client.prepare_papi_var(origin_y),
            origin_z=self._papi_client.prepare_papi_var(origin_z),
            target_x=self._papi_client.prepare_papi_var(target_x),
            target_y=self._papi_client.prepare_papi_var(target_y),
            target_z=self._papi_client.prepare_papi_var(target_z),
        )

        # No raw method for target line
        target_line_data = find_by_uuid(
            value=target_line_id['uuid'],
            input_list=self._papi_client.get_well_target_lines_data(well_id=self.uuid),
        )

        if self._target_lines is not None:
            self._target_lines.append(TargetLine(**target_line_data))

    def update_meta(
        self,
        name: Optional[str] = keep_value,
        operator: Optional[str] = keep_value,
        api: Optional[str] = keep_value,
        xsrf: Optional[float] = keep_value,
        ysrf: Optional[float] = keep_value,
        kb: Optional[float] = keep_value,
        azimuth: Optional[float] = keep_value,
        convergence: Optional[float] = keep_value,
        tie_in_tvd: Optional[float] = keep_value,
        tie_in_ns: Optional[float] = keep_value,
        tie_in_ew: Optional[float] = keep_value,
    ):
        """
        Update metadata of this :class:`Well`.

        :param name: New name for the :class:`Well`
        :param operator: New operator for the :class:`Well`
        :param api: New API number for the :class:`Well`
        :param xsrf: New surface X coordinate for the :class:`Well`
        :param ysrf: New surface Y coordinate for the :class:`Well`
        :param kb: New Kelly Bushing (KB) elevation for the :class:`Well`
        :param azimuth: New azimuth angle for the :class:`Well`
        :param convergence: New grid convergence angle for the :class:`Well`
        :param tie_in_tvd: New True Vertical Depth (TVD) at the tie-in point
        :param tie_in_ns: New North-South coordinate at the tie-in point
        :param tie_in_ew: New East-West coordinate at the tie-in point
        :return: Updated :class:`Well` instance

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Update well metadata
            well.update_meta(
                name='NewWellName',
                operator='NewOperator',
                kb=150.0,
                azimuth=15.0
            )
        """
        is_updated = self._papi_client.update_well_meta(
            well_id=self.uuid,
            name=self.name if name is keep_value else name,
            api=self.api if api is keep_value else api,
            operator=self.operator if operator is keep_value else operator,
            xsrf=self._papi_client.prepare_papi_var(self.xsrf if xsrf is keep_value else xsrf),
            ysrf=self._papi_client.prepare_papi_var(self.ysrf if ysrf is keep_value else ysrf),
            kb=self._papi_client.prepare_papi_var(self.kb if kb is keep_value else kb),
            azimuth=self._papi_client.prepare_papi_var(self.azimuth if azimuth is keep_value else azimuth),
            convergence=self._papi_client.prepare_papi_var(
                self.convergence if convergence is keep_value else convergence
            ),
            tie_in_tvd=self._papi_client.prepare_papi_var(self.tie_in_tvd if tie_in_tvd is keep_value else tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(self.tie_in_ns if tie_in_ns is keep_value else tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(self.tie_in_ew if tie_in_ew is keep_value else tie_in_ew),
        )

        if is_updated:
            well_data = self._papi_client.get_project_well_data(well_id=self.uuid)
            self.__dict__.update(**well_data)

        return self


class WellAttributes(BaseObject):
    """
    Represent attributes of a :class:`~rogii_solo.well.Well`, providing access to various well properties
    and their values.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')

        # Get well attributes
        attributes = well.attributes

        # Convert attributes to dictionary
        attrs_dict = attributes.to_dict()
        print(attrs_dict)

        # Convert attributes to DataFrame
        attrs_df = attributes.to_df()
        print(attrs_df)
    """

    def __init__(self, well: Well, **kwargs):
        self.well = well
        """Reference to the :class:`~rogii_solo.well.Well` instance these attributes belong to."""

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict:
        """
        Convert the :class:`WellAttributes` instance to a dictionary.

        :param get_converted: Whether to convert values to project units
        :return: Dictionary representation of the :class:`WellAttributes`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            attributes = well.attributes

            # Get attributes to dictionary with unit conversion
            attrs_dict = attributes.to_dict()
            print(attrs_dict)

            # Get raw attribute to dictionary without conversion
            attrs_dict = attributes.to_dict(get_converted=False)
            print(attrs_dict)
        """
        measure_units = self.well.project.measure_unit
        data = self.__dict__
        result = {}

        for k, v in data.items():
            if k == 'KB':
                result[k] = (
                    self.safe_round(self.convert_z(value=data['KB'], measure_units=measure_units))
                    if get_converted
                    else data['KB']
                )
            elif k == 'Azimuth VS':
                result[k] = (
                    self.safe_round(self.convert_angle(data['Azimuth VS'])) if get_converted else data['Azimuth VS']
                )
            elif k == 'Convergence':
                result[k] = (
                    self.safe_round(self.convert_angle(data['Convergence'])) if get_converted else data['Convergence']
                )
            elif k == 'X-srf':
                result[k] = self.safe_round(data['X-srf']) if get_converted else feet_to_meters(data['X-srf'])
            elif k == 'Y-srf':
                result[k] = self.safe_round(data['Y-srf']) if get_converted else feet_to_meters(data['Y-srf'])
            elif k == 'well':
                continue
            else:
                result[k] = v

        return result

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`WellAttributes` instance to a Pandas DataFrame.

        :param get_converted: Whether to convert values to project units
        :return: DataFrame representation of the :class:`WellAttributes`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            attributes = well.attributes

            # Get attributes to DataFrame with unit conversion
            attrs_dict = attributes.to_dict()
            print(attrs_dict)

            # Get raw attribute to DataFrame without conversion
            attrs_dict = attributes.to_dict(get_converted=False)
            print(attrs_dict)
        """
        return DataFrame(self.to_dict(get_converted), index=[0])


class NestedWell(ComplexObject):
    """
    Represent a well plan within a parent :class:`~rogii_solo.well.Well`. Contains all well plans' data
    and operations including trajectory, topsets, and more.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')

        # Get well plans
        well_plans = well.nested_wells

        # Get a specific well plan
        well_plan = well_planss.find_by_name('WellPlan1')

        # Get well plan attributes
        print(f'Well plan name: {well_plan.name}')
        print(f'Well plan API: {well_plan.api}')
        print(f'Well plan operator: {well_plan.operator}')
        print(f'Well plan KB: {well_plan.kb}')
        print(f'Well plan surface coordinates: ({well_plan.xsrf}, {well_plan.ysrf})')
    """

    def __init__(self, papi_client: PapiClient, well: Well, **kwargs):
        super().__init__(papi_client)

        self.well = well
        """The :class:`~rogii_solo.well.Well` this :class:`NestedWell` belongs to."""

        self.project = well.project
        """The :class:`~rogii_solo.project.Project` this :class:`NestedWell` belongs to."""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`NestedWell`."""

        self.name: Optional[str] = None
        """Name of the :class:`NestedWell`."""

        self.xsrf: Optional[float] = None
        """Surface X-coordinate of the :class:`NestedWell`."""

        self.ysrf: Optional[float] = None
        """Surface Y-coordinate of the :class:`NestedWell`."""

        self.xsrf_real: Optional[float] = None
        """Real surface X-coordinate of the :class:`NestedWell`."""

        self.ysrf_real: Optional[float] = None
        """Real surface Y-coordinate of the :class:`NestedWell`."""

        self.kb: Optional[float] = None
        """Kelly Bushing (KB) elevation of the :class:`NestedWell`."""

        self.api: Optional[str] = None
        """API number of the :class:`NestedWell`."""

        self.operator: Optional[str] = None
        """Operator of the :class:`NestedWell`."""

        self.azimuth: Optional[float] = None
        """Azimuth angle of the :class:`NestedWell` in degrees."""

        self.convergence: Optional[float] = None
        """Grid convergence angle of the :class:`NestedWell` in degrees."""

        self.tie_in_tvd: Optional[float] = None
        """True Vertical Depth (TVD) at the tie-in point."""

        self.tie_in_ns: Optional[float] = None
        """North-South coordinate at the tie-in point."""

        self.tie_in_ew: Optional[float] = None
        """East-West coordinate at the tie-in point."""

        self.starred: Optional[bool] = None
        """Whether this :class:`NestedWell` is starred."""

        self.__dict__.update(kwargs)

        self.kb = 0 if self.kb is None else self.kb
        self.tie_in_ns = 0 if self.tie_in_ns is None else self.tie_in_ns
        self.tie_in_ew = 0 if self.tie_in_ew is None else self.tie_in_ew

        self._trajectory: Optional[TrajectoryPointRepository[TrajectoryPoint]] = None
        self._topsets: Optional[ObjectRepository[Topset]] = None
        self._starred_topset: Optional[Topset] = None

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        """
        Get the trajectory data for this :class:`NestedWell`.

        :return: A :class:`TrajectoryPointRepository` containing the well plan's trajectory points.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            well_plan = well.nested_wells.find_by_name('WellPlan1')

            # Get the well plan's trajectory
            trajectory = well_plan.trajectory
            print(trajectory.to_dict())
        """
        if self._trajectory is None:
            self._trajectory = TrajectoryPointRepository(
                objects=[
                    TrajectoryPoint(measure_units=self.well.project.measure_unit, **item)
                    for item in self._papi_client.get_nested_well_trajectory_data(nested_well_id=self.uuid)
                ]
            )

        return self._trajectory

    @property
    def topsets(self) -> ObjectRepository[Topset]:
        """
        Get the topsets associated with this :class:`NestedWell`.

        :return: An :class:`ObjectRepository` containing :class:`~rogii_solo.topset.Topset` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            well_plan = well.nested_wells.find_by_name('WellPlan1')

            # Get all topsets
            topsets = well_plan.topsets
            print(topsets.to_dict())

            # Find a specific topset
            topset = topsets.find_by_name('Topset1')
            print(topset.to_dict())
        """
        if self._topsets is None:
            self._topsets = ObjectRepository(
                objects=[
                    Topset(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_nested_well_topsets_data(nested_well_id=self.uuid)
                ]
            )

        return self._topsets

    @property
    def starred_topset(self) -> Optional[Topset]:
        """
        Get the starred topset for this :class:`NestedWell`.

        :return: The starred :class:`~rogii_solo.topset.Topset` instance, or None if none is starred.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            well_plan = well.nested_wells.find_by_name('WellPlan1')

            # Get the starred topset
            starred = well_plan.starred_topset

            if starred:
                print(starred.to_dict())
        """
        if self._starred_topset is None:
            starred_topset_id = self._find_by_path(obj=self.starred, path='topset')
            self._starred_topset = self.topsets.find_by_id(starred_topset_id)

        return self._starred_topset

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`NestedWell` instance to a dictionary.

        :param get_converted: Whether to convert values to project units
        :return: Dictionary representation of the :class:`NestedWell`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            well_plan = well.nested_wells.find_by_name('WellPlan1')

            # Convert the well plan to a dictionary with unit conversion
            well_plan_dict = well_plan.to_dict()
            print(well_planl_dict)

            # Convert the well plan to a dictionary without unit conversion
            raw_dict = well_plan.to_dict(get_converted=False)
            print(raw_dict)
        """
        measure_units = self.well.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'api': self.api,
            'operator': self.operator,
            'xsrf': (
                self.safe_round(self.convert_xy(value=self.xsrf, measure_units=measure_units, force_to_meters=True))
                if get_converted
                else self.xsrf
            ),
            'ysrf': (
                self.safe_round(self.convert_xy(value=self.ysrf, measure_units=measure_units, force_to_meters=True))
                if get_converted
                else self.ysrf
            ),
            'xsrf_real': self.safe_round(self.xsrf_real) if get_converted else feet_to_meters(self.xsrf_real),
            'ysrf_real': self.safe_round(self.ysrf_real) if get_converted else feet_to_meters(self.ysrf_real),
            'kb': (
                self.safe_round(self.convert_z(value=self.kb, measure_units=measure_units))
                if get_converted
                else self.kb
            ),
            'azimuth': self.safe_round(self.convert_angle(self.azimuth)) if get_converted else self.azimuth,
            'convergence': self.safe_round(self.convert_angle(self.convergence)) if get_converted else self.convergence,
            'tie_in_tvd': (
                self.safe_round(self.convert_z(value=self.tie_in_tvd, measure_units=measure_units))
                if get_converted
                else self.tie_in_tvd
            ),
            'tie_in_ns': (
                self.safe_round(self.convert_xy(value=self.tie_in_ns, measure_units=measure_units))
                if get_converted
                else self.tie_in_ns
            ),
            'tie_in_ew': (
                self.safe_round(self.convert_xy(value=self.tie_in_ew, measure_units=measure_units))
                if get_converted
                else self.tie_in_ew
            ),
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`NestedWell` instance to a Pandas DataFrame.

        :param get_converted: Whether to convert values to project units
        :return: DataFrame representation of the :class:`NestedWell`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            well_plan = well.nested_wells.find_by_name('WellPlan1')

            # Convert the well plan to a DataFrame
            well_plan_df = well_plan.to_df()
            print(well_plan_df)
        """
        return DataFrame([self.to_dict(get_converted)])

    def replace_trajectory(self, md_uom: str, incl_uom: str, azi_uom: str, trajectory_stations: DataList):
        """
        Replace the trajectory data for this :class:`NestedWell`.

        :param md_uom: Unit of measurement for measured depth values
        :param incl_uom: Unit of measurement for inclination values
        :param azi_uom: Unit of measurement for azimuth values
        :param trajectory_stations: List of trajectory points data

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            well_plan = well.nested_wells.find_by_name('WellPlan1')

            # Replace the well plan's trajectory
            trajectory_data = [
                {'md': 0, 'incl': 0, 'azim': 0},
                {'md': 1000, 'incl': 45, 'azim': 180},
            ]
            well_plan.replace_trajectory(
                md_uom='ft',
                incl_uom='deg',
                azi_uom='deg',
                trajectory_stations=trajectory_data
            )
        """
        prepared_trajectory_stations = [
            {key: self._papi_client.prepare_papi_var(value) for key, value in point.items()}
            for point in trajectory_stations
        ]

        self._papi_client.replace_nested_well_trajectory(
            nested_well_id=self.uuid,
            md_uom=md_uom,
            incl_uom=incl_uom,
            azi_uom=azi_uom,
            trajectory_stations=prepared_trajectory_stations,
        )

        self._trajectory = None

    def create_topset(self, name: str):
        """
        Create a new topset in this :class:`NestedWell`.

        :param name: Name of the topset

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            well_plan = well.nested_wells.find_by_name('WellPlan1')

            # Create a new topset
            well_plan.create_topset('Topset1')
        """
        topset_id = self._papi_client.create_nested_well_topset(nested_well_id=self.uuid, name=name)

        if self._topsets is not None:
            self._topsets.append(
                Topset(
                    papi_client=self._papi_client,
                    well=self,
                    uuid=topset_id['uuid'],
                    name=name,
                )
            )

    def update_meta(
        self,
        name: Optional[str] = None,
        operator: Optional[str] = None,
        api: Optional[str] = None,
        xsrf: Optional[float] = None,
        ysrf: Optional[float] = None,
        kb: Optional[float] = None,
        tie_in_tvd: Optional[float] = None,
        tie_in_ns: Optional[float] = None,
        tie_in_ew: Optional[float] = None,
    ) -> 'NestedWell':
        """
        Update metadata of this :class:`NestedWell`.

        :param name: New name for the :class:`NestedWell`
        :param operator: New operator for the :class:`NestedWell`
        :param api: New API number for the :class:`NestedWell`
        :param xsrf: New surface X-coordinate for the :class:`NestedWell`
        :param ysrf: New surface Y-coordinate for the :class:`NestedWell`
        :param kb: New Kelly Bushing (KB) elevation for the :class:`NestedWell`
        :param tie_in_tvd: New True Vertical Depth (TVD) at the tie-in point
        :param tie_in_ns: New North-South coordinate at the tie-in point
        :param tie_in_ew: New East-West coordinate at the tie-in point

        :return: Updated :class:`NestedWell` instance

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            well_plan = well.nested_wells.find_by_name('WellPlan1')

            # Update well plan metadata
            well_plan.update_meta(
                name='WellPlan2',
                operator='NewOperator',
                kb=150.0
            )
        """
        is_updated = self._papi_client.update_nested_well_meta(
            well_id=self.uuid,
            name=name,
            api=api,
            operator=operator,
            xsrf=self._papi_client.prepare_papi_var(xsrf),
            ysrf=self._papi_client.prepare_papi_var(ysrf),
            kb=self._papi_client.prepare_papi_var(kb),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew),
        )

        if is_updated:
            # No raw method for nested well
            nested_well_data = find_by_uuid(
                value=self.uuid,
                input_list=self._papi_client.get_well_nested_wells_data(well_id=self.well.uuid, query=name),
            )
            self.__dict__.update(**nested_well_data)

        return self


class Typewell(ComplexObject):
    """
    Represent a :class:`~rogii_solo.well.Typewell` in a :class:`~rogii_solo.project.Project`.
    Contains all type well-related data and operations including trajectory, logs, topsets, mudlogs and more.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')

        # Get linked type wells
        type_wells = well.linked_typewells

        # Get a specific type well
        type_well = type_wells.find_by_name('TypeWell1')

        # Get type well attributes
        print(f"Type well name: {type_well.name}")
        print(f"Type well API: {type_well.api}")
        print(f"Type well operator: {type_well.operator}")
        print(f"Type well KB: {type_well.kb}")
        print(f"Type well surface coordinates: ({type_well.xsrf}, {type_well.ysrf})")
    """

    def __init__(self, papi_client: PapiClient, project: 'rogii_solo.project.Project', **kwargs):
        super().__init__(papi_client)

        self.project = project
        """The :class:`~rogii_solo.project.Project` this :class:`~rogii_solo.well.Typewell` belongs to."""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`~rogii_solo.well.Typewell`."""

        self.name: Optional[str] = None
        """Name of the :class:`~rogii_solo.well.Typewell`."""

        self.api: Optional[str] = None
        """API number of the :class:`~rogii_solo.well.Typewell`."""

        self.kb: Optional[float] = None
        """Kelly Bushing (KB) elevation of the :class:`~rogii_solo.well.Typewell`."""

        self.operator: Optional[str] = None
        """Operator of the :class:`~rogii_solo.well.Typewell`."""

        self.xsrf: Optional[float] = None
        """Surface X coordinate of the :class:`~rogii_solo.well.Typewell`."""

        self.ysrf: Optional[float] = None
        """Surface Y coordinate of the :class:`~rogii_solo.well.Typewell`."""

        self.xsrf_real: Optional[float] = None
        """Real surface X coordinate of the :class:`~rogii_solo.well.Typewell`."""

        self.ysrf_real: Optional[float] = None
        """Real surface Y coordinate of the :class:`~rogii_solo.well.Typewell`."""

        self.convergence: Optional[float] = None
        """Grid convergence angle of the :class:`~rogii_solo.well.Typewell` in degrees."""

        self.tie_in_tvd: Optional[float] = None
        """True Vertical Depth (TVD) at the tie-in point."""

        self.tie_in_ns: Optional[float] = None
        """North-South coordinate at the tie-in point."""

        self.tie_in_ew: Optional[float] = None
        """East-West coordinate at the tie-in point."""

        self.starred: Optional[bool] = None
        """Whether this :class:`~rogii_solo.well.Typewell` is starred."""

        self.shift: Optional[float] = None
        """Shift value applied to this :class:`~rogii_solo.well.Typewell`."""

        self.__dict__.update(kwargs)

        self.kb = 0 if self.kb is None else self.kb
        self.tie_in_ns = 0 if self.tie_in_ns is None else self.tie_in_ns
        self.tie_in_ew = 0 if self.tie_in_ew is None else self.tie_in_ew

        self._trajectory: Optional[TrajectoryPointRepository[TrajectoryPoint]] = None
        self._logs: Optional[ObjectRepository[Log]] = None
        self._topsets: Optional[ObjectRepository[Topset]] = None
        self._starred_topset: Optional[Topset] = None
        self._mudlogs: Optional[ObjectRepository[Mudlog]] = None

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        """
        Get the trajectory data for this :class:`~rogii_solo.well.Typewell`.

        :return: A :class:`TrajectoryPointRepository` containing the :class:`~rogii_solo.well.Typewell`
        trajectory points.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Get the type well's trajectory
            trajectory = type_well.trajectory
            print(trajectory.to_dict())
        """
        if self._trajectory is None:
            self._trajectory = TrajectoryPointRepository(
                objects=[
                    TrajectoryPoint(measure_units=self.project.measure_unit, **item)
                    for item in self._papi_client.get_typewell_trajectory_data(typewell_id=self.uuid)
                ]
            )

        return self._trajectory

    @property
    def logs(self) -> ObjectRepository[Log]:
        """
        Get the list of :class:`~rogii_solo.log.Log` instances associated with this :class:`~rogii_solo.well.Typewell`.

        :return: An :class:`~rogii_solo.base.ObjectRepository` containing :class:`~rogii_solo.log.Log` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Get all logs
            logs = type_well.logs
            print(logs.to_dict())

            # Find a specific log
            log = logs.find_by_name('Log1')
            print(log.to_dict())
        """
        if self._logs is None:
            self._logs = ObjectRepository(
                objects=[
                    Log(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_typewell_logs_data(typewell_id=self.uuid)
                ]
            )

        return self._logs

    @property
    def topsets(self) -> ObjectRepository[Topset]:
        """
        Get the list of :class:`~rogii_solo.topset.Topset` instances
        associated with this :class:`~rogii_solo.well.Typewell`.

        :return: An :class:`~rogii_solo.base.ObjectRepository` containing :class:`~rogii_solo.topset.Topset` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Get all topsets
            topsets = type_well.topsets
            print(topsets.to_dict())

            # Find a specific topset
            topset = topsets.find_by_name('Topset1')
            print(topset.to_dict())
        """
        if self._topsets is None:
            self._topsets = ObjectRepository(
                objects=[
                    Topset(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_typewell_topsets_data(typewell_id=self.uuid)
                ]
            )

        return self._topsets

    @property
    def starred_topset(self) -> Optional[Topset]:
        """
        Get the starred :class:`~rogii_solo.topset.Topset` for this :class:`~rogii_solo.well.Typewell`.

        :return: The starred :class:`~rogii_solo.topset.Topset` instance, or None if none is starred.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Get the starred topset
            starred = type_well.starred_topset

            if starred:
                print(starred.to_dict())
        """
        if self._starred_topset is None:
            starred_topset_id = self._find_by_path(obj=self.starred, path='topset')
            self._starred_topset = self.topsets.find_by_id(starred_topset_id)

        return self._starred_topset

    @property
    def mudlogs(self) -> ObjectRepository[Mudlog]:
        """
        Get the list of :class:`~rogii_solo.mudlog.Mudlog` instances
        associated with this :class:`~rogii_solo.well.Typewell`.

        :return: An :class:`ObjectRepository` containing :class:`~rogii_solo.mudlog.Mudlog` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Get all mudlogs
            mudlogs = type_well.mudlogs
            print(mudlogs.to_dict())

            # Find a specific mudlog
            mudlog = mudlogs.find_by_name('Mudlog1')
            print(mudlog.to_dict())
        """
        if self._mudlogs is None:
            self._mudlogs = ObjectRepository(
                objects=[
                    Mudlog(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_typewell_mudlogs_data(typewell_id=self.uuid)
                ]
            )

        return self._mudlogs

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`~rogii_solo.well.Typewell` instance to a dictionary.

        :param get_converted: Whether to convert values to project units
        :return: Dictionary representation of the :class:`~rogii_solo.well.Typewell`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Convert the type well to a dictionary with unit conversion
            type_well_dict = type_well.to_dict()
            print(type_well_dict)

            # Convert the type well to a dictionary without unit conversion
            raw_dict = type_well.to_dict(get_converted=False)
            print(raw_dict)
        """
        measure_units = self.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'api': self.api,
            'operator': self.operator,
            'xsrf': (
                self.safe_round(self.convert_xy(value=self.xsrf, measure_units=measure_units, force_to_meters=True))
                if get_converted
                else self.xsrf
            ),
            'ysrf': (
                self.safe_round(self.convert_xy(value=self.ysrf, measure_units=measure_units, force_to_meters=True))
                if get_converted
                else self.ysrf
            ),
            'xsrf_real': self.safe_round(self.xsrf_real) if get_converted else feet_to_meters(self.xsrf_real),
            'ysrf_real': self.safe_round(self.ysrf_real) if get_converted else feet_to_meters(self.ysrf_real),
            'kb': (
                self.safe_round(self.convert_z(value=self.kb, measure_units=measure_units))
                if get_converted
                else self.kb
            ),
            'convergence': self.safe_round(self.convert_angle(self.convergence)) if get_converted else self.convergence,
            'tie_in_tvd': (
                self.safe_round(self.convert_z(value=self.tie_in_tvd, measure_units=measure_units))
                if get_converted
                else self.tie_in_tvd
            ),
            'tie_in_ns': (
                self.safe_round(self.convert_xy(value=self.tie_in_ns, measure_units=measure_units))
                if get_converted
                else self.tie_in_ns
            ),
            'tie_in_ew': (
                self.safe_round(self.convert_xy(value=self.tie_in_ew, measure_units=measure_units))
                if get_converted
                else self.tie_in_ew
            ),
            # Shift is returned in project units
            'shift': self.safe_round(self.shift) if get_converted else feet_to_meters(value=self.shift),
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`~rogii_solo.well.Typewell` instance to a Pandas DataFrame.

        :param get_converted: Whether to convert values to project units
        :return: DataFrame representation of the :class:`~rogii_solo.well.Typewell`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Convert the type well to a DataFrame
            type_well_df = type_well.to_df()
            print(type_well_df)
        """
        return DataFrame([self.to_dict(get_converted)])

    def update_meta(
        self,
        name: Optional[str] = None,
        operator: Optional[str] = None,
        api: Optional[str] = None,
        xsrf: Optional[float] = None,
        ysrf: Optional[float] = None,
        kb: Optional[float] = None,
        convergence: Optional[float] = None,
        tie_in_tvd: Optional[float] = None,
        tie_in_ns: Optional[float] = None,
        tie_in_ew: Optional[float] = None,
    ) -> 'Typewell':
        """
        Update metadata of this :class:`~rogii_solo.well.Typewell`.

        :param name: New name for the :class:`~rogii_solo.well.Typewell`
        :param operator: New operator for the :class:`~rogii_solo.well.Typewell`
        :param api: New API number for the :class:`~rogii_solo.well.Typewell`
        :param xsrf: New surface X-coordinate for the :class:`~rogii_solo.well.Typewell`
        :param ysrf: New surface Y-coordinate for the :class:`~rogii_solo.well.Typewell`
        :param kb: New Kelly Bushing (KB) elevation for the :class:`~rogii_solo.well.Typewell`
        :param convergence: New grid convergence angle for the :class:`~rogii_solo.well.Typewell`
        :param tie_in_tvd: New True Vertical Depth (TVD) at the tie-in point
        :param tie_in_ns: New North-South coordinate at the tie-in point
        :param tie_in_ew: New East-West coordinate at the tie-in point
        :return: Updated :class:`~rogii_solo.well.Typewell` instance

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Update type well metadata
            type_well.update_meta(
                name='NewTypeWellName',
                operator='NewOperator',
                kb=150.0,
                convergence=0.2
            )
        """
        is_updated = self._papi_client.update_typewell_meta(
            well_id=self.uuid,
            name=name,
            api=api,
            operator=operator,
            xsrf=self._papi_client.prepare_papi_var(xsrf),
            ysrf=self._papi_client.prepare_papi_var(ysrf),
            kb=self._papi_client.prepare_papi_var(kb),
            convergence=self._papi_client.prepare_papi_var(convergence),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew),
        )

        if is_updated:
            # No raw method for typewell
            typewell_data = find_by_uuid(
                value=self.uuid,
                input_list=self._papi_client.get_project_typewells_data(project_id=self.project.uuid, query=name),
            )
            self.__dict__.update(**typewell_data)

        return self

    def create_topset(self, name: str):
        """
        Create a new :class:`~rogii_solo.topset.Topset` in this :class:`~rogii_solo.well.Typewell`.

        :param name: Name of the :class:`~rogii_solo.topset.Topset`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Create a new topset
            type_well.create_topset('Topset1')
        """
        topset_id = self._papi_client.create_typewell_topset(typewell_id=self.uuid, name=name)

        if self._topsets is not None:
            self._topsets.append(
                Topset(
                    papi_client=self._papi_client,
                    well=self,
                    uuid=topset_id['uuid'],
                    name=name,
                )
            )

    def create_log(self, name: str, points: DataList):
        """
        Create a new :class:`~rogii_solo.log.Log` in this :class:`~rogii_solo.well.Typewell`.

        :param name: Name of the :class:`~rogii_solo.log.Log`
        :param points: List of :class:`~rogii_solo.log.Log` points data

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            type_well = well.linked_typewells.find_by_name('TypeWell1')

            # Create a new log with some points
            points = [
                {'md': 0, 'value': 100},
                {'md': 100, 'value': 200},
                {'md': 200, 'value': 300}
            ]
            type_well.create_log(name='Log1', points=points)
        """
        log_id = self._papi_client.create_typewell_log(typewell_id=self.uuid, name=name)
        prepared_points = [
            {key: self._papi_client.prepare_papi_var(value) for key, value in point.items()} for point in points
        ]
        units = ELogMeasureUnits.convert_from_measure_units(self.project.measure_unit)

        self._papi_client.replace_log(log_id=log_id['uuid'], index_unit=units, log_points=prepared_points)

        if self._logs is not None:
            self._logs.append(
                Log(
                    papi_client=self._papi_client,
                    well=self,
                    uuid=log_id['uuid'],
                    name=name,
                )
            )
