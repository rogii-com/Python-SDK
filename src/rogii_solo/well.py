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
    def __init__(self, papi_client: PapiClient, project: 'rogii_solo.project.Project', **kwargs):
        super().__init__(papi_client)

        self.project = project

        self.uuid = None
        self.name = None
        self.xsrf = None
        self.ysrf = None
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

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
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
        return DataFrame([self.to_dict(get_converted)])

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        if self._trajectory is None:
            self._trajectory = TrajectoryPointRepository(
                objects=[
                    TrajectoryPoint(measure_units=self.project.measure_unit, **item)
                    for item in self._papi_client.get_well_trajectory_data(well_id=self.uuid)
                ]
            )

        return self._trajectory

    def replace_trajectory(self, md_uom: str, incl_uom: str, azi_uom: str, trajectory_stations: DataList):
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

    @property
    def interpretations(self) -> ObjectRepository[Interpretation]:
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
        if self._starred_interpretation is None:
            starred_interpretation_id = self._find_by_path(obj=self.starred, path='interpretation')
            self._starred_interpretation = self.interpretations.find_by_id(starred_interpretation_id)

        return self._starred_interpretation

    @property
    def target_lines(self) -> ObjectRepository[TargetLine]:
        if self._target_lines is None:
            self._target_lines = ObjectRepository(
                objects=[TargetLine(**item) for item in self._papi_client.get_well_target_lines_data(well_id=self.uuid)]
            )

        return self._target_lines

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
                    for item in self._papi_client.get_well_nested_wells_data(well_id=self.uuid)
                ]
            )

        return self._nested_wells

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
        linked_typewells_data = []
        project_typewells_data = self._papi_client.get_project_typewells_data(project_id=self.project.uuid)
        well_typewells_data = self._papi_client.get_well_linked_typewells_data(well_id=self.uuid)

        def get_shift(typewell_id: str, typewells_data: DataList) -> Optional[float]:
            for typewell_data in typewells_data:
                if typewell_data['typewell_id'] == typewell_id:
                    return typewell_data['shift']

        for typewell_data in project_typewells_data:
            shift = get_shift(typewell_id=typewell_data['uuid'], typewells_data=well_typewells_data)

            if shift is not None:
                linked_typewells_data.append({**typewell_data, 'shift': shift})

        return linked_typewells_data

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
                objects=[
                    Log(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_well_logs_data(well_id=self.uuid)
                ]
            )

        return self._logs

    @property
    def topsets(self) -> ObjectRepository[Topset]:
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
        if self._starred_topset is None:
            starred_topset_id = self._find_by_path(obj=self.starred, path='topset')
            self._starred_topset = self.topsets.find_by_id(starred_topset_id)

        return self._starred_topset

    @property
    def mudlogs(self) -> ObjectRepository[Mudlog]:
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
        if self._attributes is None:
            self._attributes = WellAttributes(well=self, **self._get_attributes_data())

        return self._attributes

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
        topset_id = self._papi_client.create_well_topset(well_id=self.uuid, name=name)

        if self._topsets is not None:
            self._topsets.append(Topset(papi_client=self._papi_client, well=self, uuid=topset_id, name=name))

    def create_log(self, name: str, points: DataList):
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
    def __init__(self, well: Well, **kwargs):
        self.well = well

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict:
        measure_units = self.well.project.measure_unit
        data = self.__dict__

        return {
            'Name': data['Name'],
            'API': data['API'],
            'Operator': data['Operator'],
            'KB': (
                self.safe_round(self.convert_z(value=data['KB'], measure_units=measure_units))
                if get_converted
                else data['KB']
            ),
            'Azimuth VS': (
                self.safe_round(self.convert_angle(data['Azimuth VS'])) if get_converted else data['Azimuth VS']
            ),
            'Convergence': (
                self.safe_round(self.convert_angle(data['Convergence'])) if get_converted else data['Convergence']
            ),
            'X-srf': self.safe_round(data['X-srf']) if get_converted else feet_to_meters(data['X-srf']),
            'Y-srf': self.safe_round(data['Y-srf']) if get_converted else feet_to_meters(data['Y-srf']),
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame(self.to_dict(get_converted), index=[0])


class NestedWell(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: Well, **kwargs):
        super().__init__(papi_client)

        self.well = well
        self.project = well.project

        self.uuid = None
        self.name = None
        self.xsrf = None
        self.ysrf = None
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

        self.kb = 0 if self.kb is None else self.kb
        self.tie_in_ns = 0 if self.tie_in_ns is None else self.tie_in_ns
        self.tie_in_ew = 0 if self.tie_in_ew is None else self.tie_in_ew

        self._trajectory: Optional[TrajectoryPointRepository[TrajectoryPoint]] = None
        self._topsets: Optional[ObjectRepository[Topset]] = None
        self._starred_topset: Optional[Topset] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
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
        return DataFrame([self.to_dict(get_converted)])

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
        if self._trajectory is None:
            self._trajectory = TrajectoryPointRepository(
                objects=[
                    TrajectoryPoint(measure_units=self.well.project.measure_unit, **item)
                    for item in self._papi_client.get_nested_well_trajectory_data(nested_well_id=self.uuid)
                ]
            )

        return self._trajectory

    def replace_trajectory(self, md_uom: str, incl_uom: str, azi_uom: str, trajectory_stations: DataList):
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

    @property
    def topsets(self) -> ObjectRepository[Topset]:
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
        if self._starred_topset is None:
            starred_topset_id = self._find_by_path(obj=self.starred, path='topset')
            self._starred_topset = self.topsets.find_by_id(starred_topset_id)

        return self._starred_topset

    def create_topset(self, name: str):
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
    ):
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
        self.xsrf_real = None
        self.ysrf_real = None
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

        self._trajectory: Optional[TrajectoryPointRepository[TrajectoryPoint]] = None
        self._logs: Optional[ObjectRepository[Log]] = None
        self._topsets: Optional[ObjectRepository[Topset]] = None
        self._starred_topset: Optional[Topset] = None
        self._mudlogs: Optional[ObjectRepository[Mudlog]] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
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
        return DataFrame([self.to_dict(get_converted)])

    @property
    def trajectory(self) -> TrajectoryPointRepository[TrajectoryPoint]:
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
        if self._starred_topset is None:
            starred_topset_id = self._find_by_path(obj=self.starred, path='topset')
            self._starred_topset = self.topsets.find_by_id(starred_topset_id)

        return self._starred_topset

    @property
    def mudlogs(self) -> ObjectRepository[Mudlog]:
        if self._mudlogs is None:
            self._mudlogs = ObjectRepository(
                objects=[
                    Mudlog(papi_client=self._papi_client, well=self, **item)
                    for item in self._papi_client.get_typewell_mudlogs_data(typewell_id=self.uuid)
                ]
            )

        return self._mudlogs

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
    ):
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
