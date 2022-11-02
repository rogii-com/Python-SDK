from typing import Any, Dict, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject
from rogii_solo.papi.client import PapiClient

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

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return self._get_data(get_converted)

    def to_df(self, get_converted: bool = True) -> DataFrame:
        data = self._get_data(get_converted)
        logs_data = data['logs']
        mudlog_data = {}

        if len(logs_data):
            first_log = logs_data[0]
            mudlog_data['MD'] = [point['md'] for point in first_log['log_points']]

            for log in logs_data:
                mudlog_data[log['name']] = [point['data'] for point in log['log_points']]

        return DataFrame(mudlog_data)

    def _get_data(self, get_converted: bool):
        meta = {
            'uuid': self.uuid,
            'name': self.name,
        }
        logs = self._get_logs(get_converted)

        return {
            'meta': meta,
            'logs': logs,
        }

    def _get_logs(self, get_converted: bool):
        logs_data = self._papi_client.get_mudlog_data(self.uuid)

        if get_converted:
            return [
                {
                    'uuid': log['uuid'],
                    'name': log['name'],
                    'log_points': [
                        {
                            'md': self.convert_z(value=log_point['md'], measure_units=self.well.project.measure_unit),
                            'data': log_point['data']
                        }
                        for log_point in log['log_points']
                    ],
                    'properties': log['properties']
                }
                for log in logs_data
            ]

        return logs_data
