from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.project
from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.calculations.enums import ELogMeasureUnits
from rogii_solo.interpretation import Interpretation
from rogii_solo.log import Log
from rogii_solo.mudlog import Mudlog
from rogii_solo.papi.client import PapiClient
from rogii_solo.target_line import TargetLine
from rogii_solo.topset import Topset
from rogii_solo.trace import TimeTrace
from rogii_solo.trajectory import TrajectoryPoint, TrajectoryPointRepository
from rogii_solo.types import DataList


class Well(ComplexObject):
    def __init__(self, papi_client: PapiClient, project: 'rogii_solo.project.Project', **kwargs):
        super().__init__(papi_client)

        self.project = project

        self.uuid = None
        self.name = None
        self.xsrf = None
        self.ysrf = None
        self.kb = None
        self.api = None
        self.operator = None
        self.azimuth = None
        self.convergence = None
        self.tie_in_tvd = None
        self.tie_in_ns = None
        self.tie_in_ew = None
        self.starred = None

        self.__dict__.update(kwargs)

        self.kb = 0 if self.kb is None else self.kb
        self.tie_in_ns = 0 if self.tie_in_ns is None else self.tie_in_ns
        self.tie_in_ew = 0 if self.tie_in_ew is None else self.tie_in_ew

        self._trajectory_data: Optional[DataList] = None
        self._trajectory: Optional[TrajectoryPointRepository[TrajectoryPoint]] = None

        self._interpretations_data: Optional[DataList] = None
        self._interpretations: Optional[ObjectRepository[Interpretation]] = None
        self._starred_interpretation: Optional[Interpretation] = None

        self._target_lines_data: Optional[DataList] = None
        self._target_lines: Optional[ObjectRepository[TargetLine]] = None
        self._starred_target_line: Optional[TargetLine] = None

        self._nested_wells_data: Optional[DataList] = None
        self._nested_wells: Optional[ObjectRepository[NestedWell]] = None
        self._starred_nested_well: Optional[NestedWell] = None

        self._logs_data: Optional[DataList] = None
        self._logs: Optional[ObjectRepository[Log]] = None

        self._topsets_data: Optional[DataList] = None
        self._topsets: Optional[ObjectRepository[Topset]] = None
        self._starred_topset:  Optional[Topset] = None

        self._mudlogs_data: Optional[DataList] = None
        self._mudlogs: Optional[ObjectRepository[Mudlog]] = None

        self._time_traces_data: Optional[DataList] = None
        self._time_traces: Optional[ObjectRepository[TimeTrace]] = None

        self._linked_typewells_data: Optional[DataList] = None
        self._linked_typewells: Optional[ObjectRepository[Typewell]] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'xsrf': self.convert_xy(
                value=self.xsrf,
                measure_units=measure_units,
                force_to_meters=True
            ) if get_converted else self.xsrf,
            'ysrf': self.convert_xy(
                value=self.ysrf,
                measure_units=measure_units,
                force_to_meters=True
            ) if get_converted else self.ysrf,
            'kb': self.convert_z(value=self.kb, measure_units=measure_units) if get_converted else self.kb,
            'api': self.api,
            'operator': self.operator,
            'azimuth': self.convert_angle(self.azimuth) if get_converted else self.azimuth,
            'convergence': self.convert_angle(self.convergence) if get_converted else self.convergence,
            'tie_in_tvd': self.convert_z(
                value=self.tie_in_tvd,
                measure_units=measure_units
            ) if get_converted else self.tie_in_tvd,
            'tie_in_ns': self.convert_xy(
                value=self.tie_in_ns,
                measure_units=measure_units
            ) if get_converted else self.tie_in_ns,
            'tie_in_ew': self.convert_xy(
                value=self.tie_in_ew,
                measure_units=measure_units
            ) if get_converted else self.tie_in_ew,
            'starred': self.starred,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        if self._trajectory is None:
            self._trajectory = TrajectoryPointRepository(
                objects=[
                    TrajectoryPoint(measure_units=self.project.measure_unit, **item)
                    for item in self._get_trajectory_data()
                ]
            )

        return self._trajectory

    def _get_trajectory_data(self) -> DataList:
        if self._trajectory_data is None:
            self._trajectory_data = self._papi_client.get_well_trajectory_data(well_id=self.uuid)

        return self._trajectory_data

    @property
    def interpretations(self) -> ObjectRepository[Interpretation]:
        if self._interpretations is None:
            self._interpretations = ObjectRepository(
                objects=[
                    Interpretation(papi_client=self._papi_client, well=self, **item)
                    for item in self._get_interpretations_data()
                ]
            )

        return self._interpretations

    def _get_interpretations_data(self) -> DataList:
        if self._interpretations_data is None:
            self._interpretations_data = self._papi_client.get_well_interpretations_data(well_id=self.uuid)

        return self._interpretations_data

    @property
    def starred_interpretation(self) -> Optional[Interpretation]:
        if self._starred_interpretation is None:
            starred_interpretation_id = self._find_by_path(obj=self.starred, path='interpretation')
            self._starred_interpretation = self.interpretations.find_by_id(starred_interpretation_id)

        return self._starred_interpretation

    @property
    def target_lines(self) -> ObjectRepository[TargetLine]:
        if self._target_lines is None:
            self._target_lines = ObjectRepository(
                objects=[TargetLine(**item) for item in self._get_target_lines_data()]
            )

        return self._target_lines

    def _get_target_lines_data(self) -> DataList:
        if self._target_lines_data is None:
            self._target_lines_data = self._papi_client.get_well_target_lines_data(well_id=self.uuid)

        return self._target_lines_data

    @property
    def starred_target_line(self) -> Optional[TargetLine]:
        if self._starred_target_line is None:
            starred_target_line_id = self._find_by_path(obj=self.starred, path='target_line')
            self._starred_target_line = self.target_lines.find_by_id(starred_target_line_id)

        return self._starred_target_line

    @property
    def nested_wells(self) -> ObjectRepository['NestedWell']:
        if self._nested_wells is None:
            self._nested_wells = ObjectRepository(
                objects=[
                    NestedWell(papi_client=self._papi_client, well=self, **item)
                    for item in self._get_nested_wells_data()
                ]
            )

        return self._nested_wells

    def _get_nested_wells_data(self) -> DataList:
        if self._nested_wells_data is None:
            self._nested_wells_data = self._papi_client.get_well_nested_wells_data(well_id=self.uuid)

        return self._nested_wells_data

    @property
    def linked_typewells(self) -> ObjectRepository['Typewell']:
        if self._linked_typewells is None:
            self._linked_typewells = ObjectRepository(
                objects=[
                    Typewell(papi_client=self._papi_client, project=self.project, **item)
                    for item in self._get_linked_typewells_data()
                ]
            )

        return self._linked_typewells

    def _get_linked_typewells_data(self) -> DataList:
        if self._linked_typewells_data is None:
            self._linked_typewells_data = []
            project_typewells_data = self._papi_client.get_project_typewells_data(project_id=self.project.uuid)
            linked_typewells_data = self._papi_client.get_well_linked_typewells_data(well_id=self.uuid)

            def get_shift(typewell_id: str, typewells_data: DataList) -> Optional[float]:
                for typewell_data in typewells_data:
                    if typewell_data['typewell_id'] == typewell_id:
                        return typewell_data['shift']

            for typewell_data in project_typewells_data:
                shift = get_shift(typewell_id=typewell_data['uuid'], typewells_data=linked_typewells_data)

                if shift is not None:
                    self._linked_typewells_data.append(
                        {
                            **typewell_data,
                            'shift': shift
                        }
                    )

        return self._linked_typewells_data

    @property
    def starred_nested_well(self) -> Optional['NestedWell']:
        if self._starred_nested_well is None:
            starred_nested_well_id = self._find_by_path(obj=self.starred, path='nested_well')
            self._starred_nested_well = self.nested_wells.find_by_id(starred_nested_well_id)

        return self._starred_nested_well

    @property
    def logs(self) -> ObjectRepository[Log]:
        if self._logs is None:
            self._logs = ObjectRepository(
                objects=[Log(papi_client=self._papi_client, well=self, **item) for item in self._get_logs_data()]
            )

        return self._logs

    def _get_logs_data(self) -> DataList:
        if self._logs_data is None:
            self._logs_data = self._papi_client.get_well_logs_data(well_id=self.uuid)

        return self._logs_data

    @property
    def topsets(self) -> ObjectRepository[Topset]:
        if self._topsets is None:
            self._topsets = ObjectRepository(
                objects=[
                    Topset(papi_client=self._papi_client, well=self, **item) for item in self._get_topsets_data()
                ]
            )

        return self._topsets

    def _get_topsets_data(self) -> DataList:
        if self._topsets_data is None:
            self._topsets_data = self._papi_client.get_well_topsets_data(well_id=self.uuid)

        return self._topsets_data

    @property
    def starred_topset(self) -> Optional[Topset]:
        if self._starred_topset is None:
            starred_topset_id = self._find_by_path(obj=self.starred, path='topset')
            self._starred_topset = self.topsets.find_by_id(starred_topset_id)

        return self._starred_topset

    @property
    def mudlogs(self) -> ObjectRepository[Mudlog]:
        if self._mudlogs is None:
            self._mudlogs = ObjectRepository(
                objects=[
                    Mudlog(papi_client=self._papi_client, well=self, **item) for item in self._get_mudlogs_data()
                ]
            )

        return self._mudlogs

    def _get_mudlogs_data(self) -> DataList:
        if self._mudlogs_data is None:
            self._mudlogs_data = self._papi_client.get_well_mudlogs_data(well_id=self.uuid)

        return self._mudlogs_data

    @property
    def time_traces(self) -> ObjectRepository[TimeTrace]:
        if self._time_traces is None:
            mapped_traces = self._get_time_traces_data()

            self._time_traces = ObjectRepository(
                objects=[
                    TimeTrace(papi_client=self._papi_client, well=self, **item)
                    for item in mapped_traces
                ]
            )

        return self._time_traces

    def _get_time_traces_data(self) -> DataList:
        if self._time_traces_data is None:
            self._time_traces_data = self._papi_client.get_well_mapped_time_traces_data(self.uuid)

        return self._time_traces_data

    def create_nested_well(self,
                           nested_well_name: str,
                           operator: str,
                           api: str,
                           xsrf: float,
                           ysrf: float,
                           kb: float,
                           tie_in_tvd: float,
                           tie_in_ns: float,
                           tie_in_ew: float
                           ):
        self._papi_client.create_well_nested_well(
            well_id=self.uuid,
            nested_well_name=nested_well_name,
            operator=operator,
            api=api,
            xsrf=self._papi_client.prepare_papi_var(xsrf),
            ysrf=self._papi_client.prepare_papi_var(ysrf),
            kb=self._papi_client.prepare_papi_var(kb),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew)
        )

        self._nested_wells_data = None
        self._nested_wells = None

    def create_topset(self, topset_name: str):
        self._papi_client.create_well_topset(
            well_id=self.uuid,
            topset_name=topset_name
        )

        self._topsets = None
        self._topsets_data = None

    def create_log(self, log_name: str, log_points: DataList):
        log_id = self._papi_client.create_well_log(
            well_id=self.uuid,
            log_name=log_name
        )

        if log_id.get('uuid') is None:
            return

        prepared_log_points = [
            {key: self._papi_client.prepare_papi_var(value) for key, value in point.items()}
            for point in log_points
        ]

        units = ELogMeasureUnits.convert_from_measure_units(self.project.measure_unit)
        self._papi_client.replace_log(
            log_id=log_id['uuid'],
            index_unit=units,
            log_points=prepared_log_points
        )

        self._logs = None
        self._logs_data = None

    def create_target_line(self,
                           target_line_name: str,
                           origin_x: float,
                           origin_y: float,
                           origin_z: float,
                           target_x: float,
                           target_y: float,
                           target_z: float
                           ):
        self._papi_client.create_well_target_line(
            well_id=self.uuid,
            target_line_name=target_line_name,
            origin_x=self._papi_client.prepare_papi_var(origin_x),
            origin_y=self._papi_client.prepare_papi_var(origin_y),
            origin_z=self._papi_client.prepare_papi_var(origin_z),
            target_x=self._papi_client.prepare_papi_var(target_x),
            target_y=self._papi_client.prepare_papi_var(target_y),
            target_z=self._papi_client.prepare_papi_var(target_z)
        )

        self._target_lines_data = None
        self._target_lines = None

    def update_meta(self,
                    name: Optional[str] = None,
                    operator: Optional[str] = None,
                    api: Optional[str] = None,
                    xsrf: Optional[float] = None,
                    ysrf: Optional[float] = None,
                    kb: Optional[float] = None,
                    azimuth: Optional[float] = None,
                    convergence: Optional[float] = None,
                    tie_in_tvd: Optional[float] = None,
                    tie_in_ns: Optional[float] = None,
                    tie_in_ew: Optional[float] = None
                    ):
        func_data = {
            func_param: func_arg
            for func_param, func_arg in locals().items()
            if func_arg is not None and func_param != 'self'
        }
        request_data = {
            key: self._papi_client.prepare_papi_var(value)
            for key, value in func_data.items()
        }

        is_updated = self._papi_client.update_well_meta(
            well_id=self.uuid,
            **request_data
        )

        if is_updated:
            self.__dict__.update(func_data)

        return self


class NestedWell(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: Well, **kwargs):
        super().__init__(papi_client)

        self.well = well
        self.project = well.project

        self.uuid = None
        self.name = None
        self.xsrf = None
        self.ysrf = None
        self.kb = None
        self.api = None
        self.operator = None
        self.azimuth = None
        self.convergence = None
        self.tie_in_tvd = None
        self.tie_in_ns = None
        self.tie_in_ew = None
        self.starred = None

        self.__dict__.update(kwargs)

        self.kb = 0 if self.kb is None else self.kb
        self.tie_in_ns = 0 if self.tie_in_ns is None else self.tie_in_ns
        self.tie_in_ew = 0 if self.tie_in_ew is None else self.tie_in_ew

        self._trajectory_data: Optional[DataList] = None
        self._trajectory: Optional[TrajectoryPointRepository[TrajectoryPoint]] = None

        self._topsets_data: Optional[DataList] = None
        self._topsets: Optional[ObjectRepository[Topset]] = None
        self._starred_topset:  Optional[Topset] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.well.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'xsrf': self.convert_xy(
                value=self.xsrf,
                measure_units=measure_units,
                force_to_meters=True
            ) if get_converted else self.xsrf,
            'ysrf': self.convert_xy(
                value=self.ysrf,
                measure_units=measure_units,
                force_to_meters=True
            ) if get_converted else self.ysrf,
            'kb': self.convert_z(value=self.kb, measure_units=measure_units) if get_converted else self.kb,
            'api': self.api,
            'operator': self.operator,
            'azimuth': self.convert_angle(self.azimuth) if get_converted else self.azimuth,
            'convergence': self.convert_angle(self.convergence) if get_converted else self.convergence,
            'tie_in_tvd': self.convert_z(
                value=self.tie_in_tvd,
                measure_units=measure_units
            ) if get_converted else self.tie_in_tvd,
            'tie_in_ns': self.convert_xy(
                value=self.tie_in_ns,
                measure_units=measure_units
            ) if get_converted else self.tie_in_ns,
            'tie_in_ew': self.convert_xy(
                value=self.tie_in_ew,
                measure_units=measure_units
            ) if get_converted else self.tie_in_ew,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        if self._trajectory is None:
            self._trajectory = TrajectoryPointRepository(
                objects=[
                    TrajectoryPoint(measure_units=self.well.project.measure_unit, **item)
                    for item in self._get_trajectory_data()
                ]
            )

        return self._trajectory

    def _get_trajectory_data(self) -> DataList:
        if self._trajectory_data is None:
            self._trajectory_data = self._papi_client.get_nested_well_trajectory_data(nested_well_id=self.uuid)

        return self._trajectory_data

    @property
    def topsets(self) -> ObjectRepository[Topset]:
        if self._topsets is None:
            self._topsets = ObjectRepository(
                objects=[
                    Topset(papi_client=self._papi_client, well=self, **item) for item in self._get_topsets_data()
                ]
            )

        return self._topsets

    def _get_topsets_data(self) -> DataList:
        if self._topsets_data is None:
            self._topsets_data = self._papi_client.get_nested_well_topsets_data(nested_well_id=self.uuid)

        return self._topsets_data

    @property
    def starred_topset(self) -> Optional[Topset]:
        if self._starred_topset is None:
            starred_topset_id = self._find_by_path(obj=self.starred, path='topset')
            self._starred_topset = self.topsets.find_by_id(starred_topset_id)

        return self._starred_topset

    def create_topset(self, topset_name: str):
        self._papi_client.create_nested_well_topset(
            nested_well_id=self.uuid,
            topset_name=topset_name
        )

        self._topsets = None
        self._topsets_data = None

    def update_meta(self,
                    name: Optional[str] = None,
                    operator: Optional[str] = None,
                    api: Optional[str] = None,
                    xsrf: Optional[float] = None,
                    ysrf: Optional[float] = None,
                    kb: Optional[float] = None,
                    tie_in_tvd: Optional[float] = None,
                    tie_in_ns: Optional[float] = None,
                    tie_in_ew: Optional[float] = None
                    ):
        func_data = {
            func_param: func_arg
            for func_param, func_arg in locals().items()
            if func_arg is not None and func_param != 'self'
        }
        request_data = {
            key: self._papi_client.prepare_papi_var(value)
            for key, value in func_data.items()
        }

        is_updated = self._papi_client.update_nested_well_meta(
            well_id=self.uuid,
            **request_data
        )

        if is_updated:
            self.__dict__.update(func_data)

        return self


class Typewell(ComplexObject):
    def __init__(self, papi_client: PapiClient, project: 'rogii_solo.project.Project', **kwargs):
        super().__init__(papi_client)

        self.project = project

        self.uuid = None
        self.name = None
        self.api = None
        self.kb = None
        self.operator = None
        self.xsrf = None
        self.ysrf = None
        self.convergence = None
        self.tie_in_tvd = None
        self.tie_in_ns = None
        self.tie_in_ew = None
        self.starred = None
        self.shift = None

        self.__dict__.update(kwargs)

        self.kb = 0 if self.kb is None else self.kb
        self.tie_in_ns = 0 if self.tie_in_ns is None else self.tie_in_ns
        self.tie_in_ew = 0 if self.tie_in_ew is None else self.tie_in_ew

        self._trajectory_data: Optional[DataList] = None
        self._trajectory: Optional[TrajectoryPointRepository[TrajectoryPoint]] = None

        self._logs_data: Optional[DataList] = None
        self._logs: Optional[ObjectRepository[Log]] = None

        self._topsets_data: Optional[DataList] = None
        self._topsets: Optional[ObjectRepository[Topset]] = None
        self._starred_topset:  Optional[Topset] = None

        self._mudlogs_data: Optional[DataList] = None
        self._mudlogs: Optional[ObjectRepository[Mudlog]] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'api': self.api,
            'xsrf': self.convert_xy(
                value=self.xsrf,
                measure_units=measure_units,
                force_to_meters=True
            ) if get_converted else self.xsrf,
            'ysrf': self.convert_xy(
                value=self.ysrf,
                measure_units=measure_units,
                force_to_meters=True
            ) if get_converted else self.ysrf,
            'kb': self.convert_z(value=self.kb, measure_units=measure_units) if get_converted else self.kb,
            'operator': self.operator,
            'convergence': self.convert_angle(self.convergence) if get_converted else self.convergence,
            'tie_in_tvd': self.convert_z(
                value=self.tie_in_tvd,
                measure_units=measure_units
            ) if get_converted else self.tie_in_tvd,
            'tie_in_ns': self.convert_xy(
                value=self.tie_in_ns,
                measure_units=measure_units
            ) if get_converted else self.tie_in_ns,
            'tie_in_ew': self.convert_xy(
                value=self.tie_in_ew,
                measure_units=measure_units
            ) if get_converted else self.tie_in_ew,
            'shift': self.convert_z(
                value=self.shift,
                measure_units=measure_units
            ) if get_converted else self.shift,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        if self._trajectory is None:
            self._trajectory = TrajectoryPointRepository(
                objects=[
                    TrajectoryPoint(measure_units=self.project.measure_unit, **item)
                    for item in self._get_trajectory_data()
                ]
            )

        return self._trajectory

    def _get_trajectory_data(self) -> DataList:
        if self._trajectory_data is None:
            self._trajectory_data = self._papi_client.get_typewell_trajectory_data(typewell_id=self.uuid)

        return self._trajectory_data

    @property
    def logs(self) -> ObjectRepository[Log]:
        if self._logs is None:
            self._logs = ObjectRepository(
                objects=[Log(papi_client=self._papi_client, well=self, **item) for item in self._get_logs_data()]
            )

        return self._logs

    def _get_logs_data(self) -> DataList:
        if self._logs_data is None:
            self._logs_data = self._papi_client.get_typewell_logs_data(typewell_id=self.uuid)

        return self._logs_data

    @property
    def topsets(self) -> ObjectRepository[Topset]:
        if self._topsets is None:
            self._topsets = ObjectRepository(
                objects=[
                    Topset(papi_client=self._papi_client, well=self, **item) for item in self._get_topsets_data()
                ]
            )

        return self._topsets

    def _get_topsets_data(self) -> Optional[DataList]:
        if self._topsets_data is None:
            self._topsets_data = self._papi_client.get_typewell_topsets_data(typewell_id=self.uuid)

        return self._topsets_data

    @property
    def starred_topset(self) -> Optional[Topset]:
        if self._starred_topset is None:
            starred_topset_id = self._find_by_path(obj=self.starred, path='topset')
            self._starred_topset = self.topsets.find_by_id(starred_topset_id)

        return self._starred_topset

    def create_topset(self, topset_name: str):
        self._papi_client.create_typewell_topset(
            typewell_id=self.uuid,
            topset_name=topset_name
        )

        self._topsets = None
        self._topsets_data = None

    def create_log(self, log_name: str, log_points: DataList):
        log_id = self._papi_client.create_typewell_log(
            typewell_id=self.uuid,
            log_name=log_name
        )

        if log_id.get('uuid') is None:
            return

        prepared_log_points = [
            {key: self._papi_client.prepare_papi_var(value) for key, value in point.items()}
            for point in log_points
        ]

        units = ELogMeasureUnits.convert_from_measure_units(self.project.measure_unit)
        self._papi_client.replace_log(
            log_id=log_id['uuid'],
            index_unit=units,
            log_points=prepared_log_points
        )

        self._logs = None
        self._logs_data = None

    @property
    def mudlogs(self) -> ObjectRepository[Mudlog]:
        if self._mudlogs is None:
            self._mudlogs = ObjectRepository(
                objects=[Mudlog(papi_client=self._papi_client, well=self, **item) for item in self._get_mudlogs_data()]
            )

        return self._mudlogs

    def _get_mudlogs_data(self) -> DataList:
        if self._mudlogs_data is None:
            self._mudlogs_data = self._papi_client.get_typewell_mudlogs_data(typewell_id=self.uuid)

        return self._mudlogs_data

    def update_meta(self,
                    name: Optional[str] = None,
                    operator: Optional[str] = None,
                    api: Optional[str] = None,
                    xsrf: Optional[float] = None,
                    ysrf: Optional[float] = None,
                    kb: Optional[float] = None,
                    convergence: Optional[float] = None,
                    tie_in_tvd: Optional[float] = None,
                    tie_in_ns: Optional[float] = None,
                    tie_in_ew: Optional[float] = None
                    ):
        func_data = {
            func_param: func_arg
            for func_param, func_arg in locals().items()
            if func_arg is not None and func_param != 'self'
        }
        request_data = {
            key: self._papi_client.prepare_papi_var(value)
            for key, value in func_data.items()
        }

        is_updated = self._papi_client.update_typewell_meta(
            well_id=self.uuid,
            **request_data
        )

        if is_updated:
            self.__dict__.update(func_data)

        return self
