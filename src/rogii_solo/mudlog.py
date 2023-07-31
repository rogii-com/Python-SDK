from typing import Dict, Optional, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ComplexObject, ObjectRepository
from rogii_solo.log import LogPoint, LogPointRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList

WellType = Union[
    'rogii_solo.well.Well',
    'rogii_solo.well.Typewell',
]


class Mudlog(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: WellType, **kwargs):
        super().__init__(papi_client)

        self.well = well

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

        self._logs: Optional['LithologyLogRepository'] = None

    def to_dict(self) -> Dict:
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        return DataFrame([self.to_dict()])

    @property
    def logs(self) -> 'LithologyLogRepository':
        if self._logs is None:
            self._logs = LithologyLogRepository(
                [
                    LithologyLog(mudlog=self, _points_data=item['log_points'], **item)
                    for item in self._papi_client.get_mudlog_data(self.uuid)
                ]
            )

        return self._logs


class LithologyLog(BaseObject):
    def __init__(self, mudlog: Mudlog, **kwargs):
        self.mudlog = mudlog

        self.uuid = None
        self.name = None
        self._points: Optional[LogPointRepository] = None
        self._points_data: Optional[DataList] = None

        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict:
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        return DataFrame([self.to_dict()])

    @property
    def points(self) -> 'LogPointRepository':
        if self._points is None:
            self._points = LogPointRepository(
                [
                    LogPoint(measure_units=self.mudlog.well.project.measure_unit, md=point['md'], value=point['data'])
                    for point in self._points_data
                ]
            )

        return self._points


class LithologyLogRepository(ObjectRepository):
    def to_df(self) -> DataFrame:
        mudlog_df = DataFrame(columns=('MD',))

        for log in self:
            log_df = log.points.to_df().rename(columns={'md': 'MD', 'value': log.name})
            mudlog_df = mudlog_df.merge(right=log_df, on='MD', how='outer')

        return mudlog_df
