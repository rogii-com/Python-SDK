from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.project
from rogii_solo.base import ComplexObject, Convertable, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.trajectory import TrajectoryPoint, TrajectoryPointRepository
from rogii_solo.types import DataList


class Typewell(ComplexObject, Convertable):
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
            self._trajectory_data = self._papi_client._get_typewell_trajectory_data(typewell_id=self.uuid)

        return self._trajectory_data

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        if not self._trajectory:
            self._trajectory = TrajectoryPointRepository(well=self, dicts=self.trajectory_data)

        return self._trajectory
