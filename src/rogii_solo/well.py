from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.project
from rogii_solo.base import BaseObject, ComplexObject, Convertable, ObjectRepository
from rogii_solo.interpretation import Interpretation
from rogii_solo.papi.client import PapiClient
from rogii_solo.target_line import TargetLine
from rogii_solo.trajectory import TrajectoryPoint, TrajectoryPointRepository
from rogii_solo.types import DataList


class Well(ComplexObject, Convertable):
    def __init__(self, papi_client: PapiClient, project: 'rogii_solo.project.Project', **kwargs):
        super().__init__(papi_client)

        self.project = project

        self.uuid = None
        self.name = None
        self.xsrf_real = None
        self.ysrf_real = None
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

        self._trajectory_data: DataList = []
        self._trajectory: TrajectoryPointRepository[TrajectoryPoint] = TrajectoryPointRepository(well=self)

        self._interpretations_data: DataList = []
        self._interpretations: ObjectRepository[Interpretation] = ObjectRepository()
        self._starred_interpretation: Optional[Interpretation] = None

        self._target_lines_data: DataList = []
        self._target_lines: ObjectRepository[TargetLine] = ObjectRepository()
        self._starred_target_line: Optional[TargetLine] = None

        self._nested_wells_data: DataList = []
        self._nested_wells: ObjectRepository[NestedWell] = ObjectRepository()
        self._starred_nested_well: Optional[NestedWell] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'xsrf_real': self.xsrf_real,
            'ysrf_real': self.ysrf_real,
            'kb': self.convert_z(self.kb, measure_units=measure_units) if get_converted else self.kb,
            'api': self.api,
            'operator': self.operator,
            'azimuth': self.convert_angle(self.azimuth) if get_converted else self.azimuth,
            'convergence': self.convert_angle(self.convergence) if get_converted else self.convergence,
            'tie_in_tvd': self.tie_in_tvd,
            'tie_in_ns': self.tie_in_ns,
            'tie_in_ew': self.tie_in_ew,
            'starred': self.starred,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])

    @property
    def trajectory_data(self) -> DataList:
        if not self._trajectory_data:
            self._trajectory_data = self._papi_client.get_well_trajectory_data(well_id=self.uuid)

        return self._trajectory_data

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        if not self._trajectory:
            self._trajectory = TrajectoryPointRepository(well=self, dicts=self.trajectory_data)

        return self._trajectory

    @property
    def interpretations_data(self) -> DataList:
        if not self._interpretations_data:
            self._interpretations_data = self._papi_client.get_well_interpretations_data(well_id=self.uuid)

        return self._interpretations_data

    @property
    def interpretations(self) -> ObjectRepository[Interpretation]:
        if not self._interpretations:
            self._interpretations = ObjectRepository(
                dicts=self.interpretations_data,
                objects=[
                    Interpretation(papi_client=self._papi_client, well=self, **item)
                    for item in self.interpretations_data
                ]
            )

        return self._interpretations

    @property
    def starred_interpretation(self) -> Optional[Interpretation]:
        if not self._starred_interpretation:
            starred_interpretation_id = self._find_by_path(self.starred, 'interpretation')
            self._starred_interpretation = self.interpretations.find_by_id(starred_interpretation_id)

        return self._starred_interpretation

    @property
    def target_lines_data(self) -> DataList:
        if not self._target_lines_data:
            self._target_lines_data = self._papi_client.get_well_target_lines_data(well_id=self.uuid)

        return self._target_lines_data

    @property
    def target_lines(self) -> ObjectRepository[TargetLine]:
        if not self._target_lines:
            self._target_lines = ObjectRepository(
                dicts=self.target_lines_data,
                objects=[TargetLine(**item) for item in self.target_lines_data]
            )

        return self._target_lines

    @property
    def starred_target_line(self) -> Optional[TargetLine]:
        if not self._starred_target_line:
            starred_target_line_id = self._find_by_path(self.starred, 'target_line')
            self._starred_target_line = self.target_lines.find_by_id(starred_target_line_id)

        return self._starred_target_line

    @property
    def nested_wells_data(self) -> DataList:
        if not self._nested_wells_data:
            self._nested_wells_data = self._papi_client.get_well_nested_wells_data(well_id=self.uuid)

        return self._nested_wells_data

    @property
    def nested_wells(self) -> ObjectRepository['NestedWell']:
        if not self._nested_wells:
            self._nested_wells = ObjectRepository(
                dicts=self.nested_wells_data,
                objects=[NestedWell(well=self, **item) for item in self.nested_wells_data]
            )

        return self._nested_wells

    @property
    def starred_nested_well(self) -> Optional['NestedWell']:
        if not self._starred_nested_well:
            starred_nested_well_id = self._find_by_path(self.starred, 'nested_well')
            self._starred_nested_well = self.nested_wells.find_by_id(starred_nested_well_id)

        return self._starred_nested_well

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

        self._nested_wells_data = []
        self._nested_wells = ObjectRepository()


class NestedWell(BaseObject, Convertable):
    def __init__(self, well: Well, **kwargs):
        self.well = well

        self.uuid = None
        self.name = None
        self.xsrf_real = None
        self.ysrf_real = None
        self.kb = None
        self.api = None
        self.operator = None
        self.azimuth = None
        self.convergence = None
        self.tie_in_tvd = None
        self.tie_in_ns = None
        self.tie_in_ew = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        measure_units = self.well.project.measure_unit

        return {
            'uuid': self.uuid,
            'name': self.name,
            'xsrf_real': self.xsrf_real,
            'ysrf_real': self.ysrf_real,
            'kb': self.convert_z(self.kb, measure_units=measure_units) if get_converted else self.kb,
            'api': self.api,
            'operator': self.operator,
            'azimuth': self.convert_angle(self.azimuth) if get_converted else self.azimuth,
            'convergence': self.convert_angle(self.convergence) if get_converted else self.convergence,
            'tie_in_tvd': self.tie_in_tvd,
            'tie_in_ns': self.tie_in_ns,
            'tie_in_ew': self.tie_in_ew,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])
