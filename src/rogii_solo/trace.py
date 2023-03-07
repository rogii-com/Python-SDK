from typing import Dict

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import Trace as TraceType


class Trace(ComplexObject):
    def __init__(self, papi_client: PapiClient, **kwargs):
        super().__init__(papi_client)

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

    def to_dict(self, *args, **kwargs) -> Dict:
        return self._get_data()

    def to_df(self, *args, **kwargs) -> TraceType:
        data = self._get_data()

        return {
            'meta': DataFrame([data['meta']]),
            'points': DataFrame(data['points']),
        }

    def _get_data(self, *args, **kwargs):
        meta = {
            'uuid': self.uuid,
            'name': self.name,
        }

        return {
            'meta': meta,
            'points': [],
        }


class TimeTrace(Trace):
    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client,  well=well, **kwargs)

        self.well = well
        self.hash = None
        self.unit = None
        self.start_date_time_index = None
        self.last_date_time_index = None

        self.__dict__.update(kwargs)

    def to_dict(self, time_from: str = None, time_to: str = None) -> Dict:
        return self._get_data(time_from=time_from, time_to=time_to)

    def to_df(self, time_from: str = None, time_to: str = None) -> TraceType:
        data = self._get_data(time_from=time_from, time_to=time_to)

        return {
            'meta': DataFrame([data['meta']]),
            'points': DataFrame(data['points']),
        }

    def _get_data(self, time_from: str = None, time_to: str = None):
        if time_from is None:
            time_from = self.start_date_time_index

        if time_to is None:
            time_to = self.last_date_time_index

        meta = {
            'uuid': self.uuid,
            'name': self.name,
            'hash': self.hash,
            'unit': self.unit,
            'start_date_time_index': self.start_date_time_index,
            'last_date_time_index': self.last_date_time_index
        }
        points = self._get_points(time_from=time_from, time_to=time_to)

        return {
            'meta': meta,
            'points': points,
        }

    def _get_points(self, time_from: str, time_to: str):
        return self._papi_client.get_well_time_trace_data(
            well_id=self.well.uuid,
            trace_id=self.uuid,
            time_from=time_from,
            time_to=time_to
        )
