from typing import Any, Dict

from pandas import DataFrame

import rogii_solo.project
from rogii_solo.base import ComplexObject, Convertable
from rogii_solo.papi.client import PapiClient
from rogii_solo.trajectory import TrajectoryPoint, TrajectoryPointRepository
from rogii_solo.types import DataList


class Typewell(ComplexObject, Convertable):
    def __init__(self, papi_client: PapiClient, project: 'rogii_solo.project.Project', **kwargs):
        super().__init__(papi_client)

        self.project = project

        self.uuid = None
        self.name = None
        self.api = None

        self.__dict__.update(kwargs)

        self._trajectory_data: DataList = []
        self._trajectory: TrajectoryPointRepository[TrajectoryPoint] = TrajectoryPointRepository(well=self)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'name': self.name,
            'api': self.api,
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
