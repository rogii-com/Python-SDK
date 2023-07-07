from typing import Any, Dict, Optional, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject
from rogii_solo.calculations.enums import ELogMeasureUnits
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList
from rogii_solo.types import Log as LogType

WellType = Union['rogii_solo.well.Well', 'rogii_solo.well.Typewell']


class Log(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: WellType, **kwargs):
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

    def replace_points(self, points: DataList):
        prepared_log_points = [
            {key: self._papi_client.prepare_papi_var(value) for key, value in point.items()} for point in points
        ]

        units = ELogMeasureUnits.convert_from_measure_units(self.well.project.measure_unit)
        self._papi_client.replace_log(log_id=self.uuid, index_unit=units, log_points=prepared_log_points)

    def update_meta(self, name: Optional[str] = None):
        func_data = {
            func_param: func_arg
            for func_param, func_arg in locals().items()
            if func_arg is not None and func_param != 'self'
        }
        request_data = {key: self._papi_client.prepare_papi_var(value) for key, value in func_data.items()}

        is_updated = self._papi_client.update_log_meta(log_id=self.uuid, **request_data)

        if is_updated:
            self.__dict__.update(func_data)

        return self
