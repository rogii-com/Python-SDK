from typing import Any, Dict

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import Log as LogType


class Log(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client)

        self.well = well

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return self._get_data(get_converted)

    def to_df(self, get_converted: bool = True) -> LogType:
        data = self._get_data(get_converted)

        return {
            'meta': DataFrame([data['meta']]),
            'points': DataFrame(data['points']),
        }

    def _get_data(self, get_converted: bool):
        meta = {
            'uuid': self.uuid,
            'name': self.name,
        }
        points = self._get_points(get_converted)

        return {
            'meta': meta,
            'points': points,
        }

    def _get_points(self, get_converted: bool):
        points_data = self._papi_client.get_log_data(self.uuid)

        if get_converted:
            return [
                {
                    'md': self.convert_z(value=point['md'], measure_units=self.well.project.measure_unit),
                    'data': point['data'],
                }
                for point in points_data
            ]

        return points_data
