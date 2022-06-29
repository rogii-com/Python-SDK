from typing import Dict, List, Optional

from pandas import DataFrame

from python_sdk.base import ComplexObject, DataFrameable, ObjectRepository
from python_sdk.interpretation import Interpretation
from python_sdk.nested_well import NestedWell
from python_sdk.target_line import TargetLine
from python_sdk.trajectory import TrajectoryPoint, TrajectoryPointList


class Well(ComplexObject, DataFrameable):
    def __init__(self, papi_client, **kwargs):
        super().__init__(papi_client)

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

        self._trajectory_data: List[Dict] = []
        self._trajectory: TrajectoryPointList[TrajectoryPoint] = TrajectoryPointList(dict_list=[])

        self._interpretations_data: List[Dict] = []
        self._interpretations: ObjectRepository[Interpretation] = ObjectRepository(dicts=[], objects=[])
        self._starred_interpretation: Optional[Interpretation] = None

        self._target_lines_data: List[Dict] = []
        self._target_lines: ObjectRepository[TargetLine] = ObjectRepository(dicts=[], objects=[])
        self._starred_target_line: Optional[TargetLine] = None

        self._nested_wells_data: List[Dict] = []
        self._nested_wells: ObjectRepository[Well] = ObjectRepository(dicts=[], objects=[])

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'xsrf_real': self.xsrf_real,
            'ysrf_real': self.ysrf_real,
            'kb': self.kb,
            'api': self.api,
            'operator': self.operator,
            'azimuth': self.azimuth,
            'convergence': self.convergence,
            'tie_in_tvd': self.tie_in_tvd,
            'tie_in_ns': self.tie_in_ns,
            'tie_in_ew': self.tie_in_ew,
            'starred': self.starred,
        }

    def to_df(self):
        return DataFrame([self.to_dict()])

    @property
    def trajectory_data(self) -> List[Dict]:
        if not self._trajectory_data:
            self._trajectory_data = [
                self._parse_papi_data(trajectory_point)
                for trajectory_point in self._papi_client.fetch_well_raw_trajectory(well_id=self.uuid)
            ]

        return self._trajectory_data

    @property
    def trajectory(self) -> TrajectoryPointList[TrajectoryPoint]:
        if not self._trajectory:
            self._trajectory = TrajectoryPointList(self.trajectory_data)

        return self._trajectory

    @property
    def interpretations_data(self) -> List[Dict]:
        if not self._interpretations_data:
            self._interpretations_data = [
                self._parse_papi_data(interpretation)
                for interpretation in self._request_all_pages(
                    func=self._papi_client.fetch_well_raw_interpretations,
                    well_id=self.uuid
                )
            ]

        return self._interpretations_data

    @property
    def interpretations(self) -> ObjectRepository[Interpretation]:
        if not self._interpretations:
            self._interpretations = ObjectRepository(
                dicts=self.interpretations_data,
                objects=[
                    Interpretation(papi_client=self._papi_client, **item) for item in self.interpretations_data
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
    def target_lines_data(self) -> List[Dict]:
        if not self._target_lines_data:
            self._target_lines_data = [
                self._parse_papi_data(target_line)
                for target_line in self._request_all_pages_with_content(
                    func=self._papi_client.fetch_well_target_lines,
                    well_id=self.uuid
                )
            ]

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
    def nested_wells_data(self) -> List[Dict]:
        if not self._nested_wells_data:
            self._nested_wells_data = [
                self._parse_papi_data(nested_well)
                for nested_well in self._request_all_pages_with_content(
                    func=self._papi_client.fetch_well_nested_wells,
                    well_id=self.uuid
                )
            ]

        return self._nested_wells_data

    @property
    def nested_wells(self) -> ObjectRepository[NestedWell]:
        if not self._nested_wells:
            self._nested_wells = ObjectRepository(
                dicts=self.nested_wells_data,
                objects=[NestedWell(**item) for item in self.nested_wells_data]
            )

        return self._nested_wells

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
        self._papi_client.create_nested_well(
            well_id=self.uuid,
            nested_well_name=nested_well_name,
            operator=operator,
            api=api,
            xsrf=self._prepare_papi_var(xsrf),
            ysrf=self._prepare_papi_var(ysrf),
            kb=self._prepare_papi_var(kb),
            tie_in_tvd=self._prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._prepare_papi_var(tie_in_ns),
            tie_in_ew=self._prepare_papi_var(tie_in_ew)
        )

        self._nested_wells_data = []
        self._nested_wells = []
