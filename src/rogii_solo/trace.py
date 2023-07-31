from abc import abstractmethod
from typing import Dict, List, Optional

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ComplexObject, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList


class Trace(ComplexObject):
    def __init__(self, papi_client: PapiClient, **kwargs):
        super().__init__(papi_client)

        self.uuid = None
        self.name = None

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
                objects=[
                    TimeTracePoint(**item)
                    for item in self._papi_client.get_well_time_trace_data(well_id=self.well.uuid, trace_id=self.uuid)
                ],
                start_date_time_index=self.start_date_time_index,
                last_date_time_index=self.last_date_time_index,
            )

        return self._points


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


class RacCode(BaseObject):
    def __init__(self, **kwargs):
        self.code = None
        self.status = None

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        return {'code': self.code, 'status': self.status}

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
