from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.project
from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.interpretation import Interpretation
from rogii_solo.log import Log
from rogii_solo.papi.client import PapiClient
from rogii_solo.target_line import TargetLine
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

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'xsrf': self.convert_xy(
                self.xsrf, measure_units=measure_units, force_to_meters=True
            ) if get_converted else self.xsrf,
            'ysrf': self.convert_xy(
                self.ysrf, measure_units=measure_units, force_to_meters=True
            ) if get_converted else self.ysrf,
            'kb': self.convert_z(self.kb, measure_units=measure_units) if get_converted else self.kb,
            'api': self.api,
            'operator': self.operator,
            'azimuth': self.convert_angle(self.azimuth) if get_converted else self.azimuth,
            'convergence': self.convert_angle(self.convergence) if get_converted else self.convergence,
            'tie_in_tvd':
                self.convert_z(self.tie_in_tvd, measure_units=measure_units) if get_converted else self.tie_in_tvd,
            'tie_in_ns':
                self.convert_xy(self.tie_in_ns, measure_units=measure_units) if get_converted else self.tie_in_ns,
            'tie_in_ew':
                self.convert_xy(self.tie_in_ew, measure_units=measure_units) if get_converted else self.tie_in_ew,
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
            starred_interpretation_id = self._find_by_path(self.starred, 'interpretation')
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
            starred_target_line_id = self._find_by_path(self.starred, 'target_line')
            self._starred_target_line = self.target_lines.find_by_id(starred_target_line_id)

        return self._starred_target_line

    @property
    def nested_wells(self) -> ObjectRepository['NestedWell']:
        if self._nested_wells is None:
            self._nested_wells = ObjectRepository(
                objects=[
                    NestedWell(
                        papi_client=self._papi_client,
                        well=self,
                        **{
                            **item,
                            'azimuth': self.azimuth,
                            'convergence': self.convergence
                        }
                    ) for item in self._get_nested_wells_data()
                ]
            )

        return self._nested_wells

    def _get_nested_wells_data(self) -> DataList:
        if self._nested_wells_data is None:
            self._nested_wells_data = self._papi_client.get_well_nested_wells_data(well_id=self.uuid)

        return self._nested_wells_data

    @property
    def starred_nested_well(self) -> Optional['NestedWell']:
        if self._starred_nested_well is None:
            starred_nested_well_id = self._find_by_path(self.starred, 'nested_well')
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


class NestedWell(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: Well, **kwargs):
        super().__init__(papi_client)

        self.well = well

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

        self.__dict__.update(kwargs)

        self.kb = 0 if self.kb is None else self.kb
        self.tie_in_ns = 0 if self.tie_in_ns is None else self.tie_in_ns
        self.tie_in_ew = 0 if self.tie_in_ew is None else self.tie_in_ew

        self._trajectory_data: Optional[DataList] = None
        self._trajectory: Optional[TrajectoryPointRepository[TrajectoryPoint]] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.well.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'xsrf': self.convert_xy(
                self.xsrf, measure_units=measure_units, force_to_meters=True
            ) if get_converted else self.xsrf,
            'ysrf': self.convert_xy(
                self.ysrf, measure_units=measure_units, force_to_meters=True
            ) if get_converted else self.ysrf,
            'kb': self.convert_z(self.kb, measure_units=measure_units) if get_converted else self.kb,
            'api': self.api,
            'operator': self.operator,
            'azimuth': self.convert_angle(self.azimuth) if get_converted else self.azimuth,
            'convergence': self.convert_angle(self.convergence) if get_converted else self.convergence,
            'tie_in_tvd':
                self.convert_z(self.tie_in_tvd, measure_units=measure_units) if get_converted else self.tie_in_tvd,
            'tie_in_ns':
                self.convert_xy(self.tie_in_ns, measure_units=measure_units) if get_converted else self.tie_in_ns,
            'tie_in_ew':
                self.convert_xy(self.tie_in_ew, measure_units=measure_units) if get_converted else self.tie_in_ew,
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
