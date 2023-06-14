from abc import abstractmethod
from typing import Dict, List, Optional

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ComplexObject
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList


class Trace(ComplexObject):
    def __init__(self, papi_client: PapiClient, **kwargs):
        super().__init__(papi_client)

        self.uuid = None
        self.name = None

        self._points_data: Optional[DataList] = None
        self._points: Optional[TracePointRepository] = None

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        return {'uuid': self.uuid, 'name': self.uuid}

    def to_df(self) -> DataFrame:
        return DataFrame([self.to_dict()])

    @property
    @abstractmethod
    def points(self) -> 'TracePointRepository':
        pass


class TimeTrace(Trace):
    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client, well=well, **kwargs)

        self.well = well

        self.hash = None
        self.unit = None
        self.start_date_time_index = None
        self.last_date_time_index = None

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        return {
            'uuid': self.uuid,
            'name': self.name,
            'hash': self.hash,
            'unit': self.unit,
            'start_date_time_index': self.start_date_time_index,
            'last_date_time_index': self.last_date_time_index,
        }

    @property
    def points(self) -> 'TimeTracePointRepository':
        if self._points is None:
            self._points = TimeTracePointRepository(
                objects=[TimeTracePoint(**item) for item in self._get_points_data()],
                start_date_time_index=self.start_date_time_index,
                last_date_time_index=self.last_date_time_index,
            )

        return self._points

    def _get_points_data(self) -> DataList:
        if self._points_data is None:
            self._points_data = self._papi_client.get_well_time_trace_data(well_id=self.well.uuid, trace_id=self.uuid)

        return self._points_data


class TimeTracePoint(BaseObject):
    def __init__(self, **kwargs):
        self.index = None
        self.value = None

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        return {'index': self.index, 'value': self.value}

    def to_df(self) -> DataFrame:
        return DataFrame([self.to_dict()])


class CalcTrace(Trace):
    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client, well=well, **kwargs)

        self.well = well

        self.hash = None
        self.start_date_time_index = None
        self.last_date_time_index = None

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        return {
            'uuid': self.uuid,
            'name': self.name,
            'hash': self.hash,
            'start_date_time_index': self.start_date_time_index,
            'last_date_time_index': self.last_date_time_index,
        }

    @property
    def points(self) -> 'CalcTracePointRepository':
        if self._points is None:
            self._points = CalcTracePointRepository(
                objects=[CalcTracePoint(**item) for item in self._get_points_data()],
                start_date_time_index=self.start_date_time_index,
                last_date_time_index=self.last_date_time_index,
            )

        return self._points

    def _get_points_data(self) -> DataList:
        if self._points_data is None:
            self._points_data = self._papi_client.get_well_calc_trace_data(well_id=self.well.uuid, trace_id=self.uuid)

        return self._points_data

    @property
    def rac_codes(self):
        return [
            {'code': 0, 'status': 'In Slips'},
            {'code': 11, 'status': 'In Slips-Pump'},
            {'code': 21, 'status': 'Drilling'},
            {'code': 22, 'status': 'Slide Drilling'},
            {'code': 23, 'status': 'Slide Oscilate Drilling'},
            {'code': 31, 'status': 'Reaming'},
            {'code': 32, 'status': 'Back Reaming'},
            {'code': 50, 'status': 'Static'},
            {'code': 51, 'status': 'Static-Rotate & Pump'},
            {'code': 52, 'status': 'Static-Pump'},
            {'code': 53, 'status': 'Static-Rotate'},
            {'code': 54, 'status': 'Surface Operations'},
            {'code': 61, 'status': 'Run In-Trip In'},
            {'code': 62, 'status': 'Run In-Pump'},
            {'code': 63, 'status': 'Run In-Rotate'},
            {'code': 64, 'status': 'Pull Up-Pump'},
            {'code': 65, 'status': 'Pull Up-Rotate'},
            {'code': 66, 'status': 'Pull Up-Trip Out'},
            {'code': 98, 'status': 'Unknown'},
            {'code': 99, 'status': 'Missing Input'},
        ]


class CalcTracePoint(BaseObject):
    def __init__(self, **kwargs):
        self.start = None
        self.end = None
        self.value = None

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        return {'start': self.start, 'end': self.end, 'value': self.value}

    def to_df(self) -> DataFrame:
        return DataFrame([self.to_dict()])


class TracePointRepository(list):
    def __init__(
        self,
        start_date_time_index: str,
        last_date_time_index: str,
        objects: List[TimeTracePoint | CalcTracePoint] = None,
    ):
        if objects is None:
            objects = []

        super().__init__(objects)

        self.start_date_time_index = start_date_time_index
        self.last_date_time_index = last_date_time_index

    @abstractmethod
    def to_dict(self, time_from: str = None, time_to: str = None) -> DataList:
        pass

    def to_df(self, time_from: str = None, time_to: str = None) -> DataFrame:
        return DataFrame(self.to_dict(time_from=time_from, time_to=time_to))


class TimeTracePointRepository(TracePointRepository):
    def to_dict(self, time_from: str = None, time_to: str = None):
        if time_from is None:
            time_from = self.start_date_time_index

        if time_to is None:
            time_to = self.last_date_time_index

        return [object_.to_dict() for object_ in self if time_from <= object_.index <= time_to]


class CalcTracePointRepository(TracePointRepository):
    def to_dict(self, time_from: str = None, time_to: str = None):
        if time_from is None:
            time_from = self.start_date_time_index

        if time_to is None:
            time_to = self.last_date_time_index

        points = []

        for object_ in self:
            points.append(object_.to_dict())

            if object_.start >= time_from and object_.end >= time_to:
                break

        return points
