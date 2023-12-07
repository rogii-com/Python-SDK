from typing import Dict, List, Optional, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ComplexObject
from rogii_solo.calculations.enums import ELogMeasureUnits, EMeasureUnits
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList

WellType = Union['rogii_solo.well.Well', 'rogii_solo.well.Typewell']


class Log(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: WellType, **kwargs):
        super().__init__(papi_client)

        self.well = well

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

        self._points: Optional[LogPointRepository] = None

    def to_dict(self) -> Dict:
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        return DataFrame([self.to_dict()])

    @property
    def points(self) -> 'LogPointRepository':
        if self._points is None:
            self._points = LogPointRepository(
                [
                    LogPoint(measure_units=self.well.project.measure_unit, md=point['md'], value=point['data'])
                    for point in self._papi_client.get_log_points(self.uuid)
                ]
            )

        return self._points

    def replace_points(self, points: DataList):
        prepared_log_points = [
            {key: self._papi_client.prepare_papi_var(value) for key, value in point.items()} for point in points
        ]
        units = ELogMeasureUnits.convert_from_measure_units(self.well.project.measure_unit)

        self._papi_client.replace_log(log_id=self.uuid, index_unit=units, log_points=prepared_log_points)
        self._points = None

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


class LogPoint(BaseObject):
    def __init__(self, measure_units: EMeasureUnits, md: float, value: float):
        self.measure_units = measure_units

        self.md = md
        self.value = value

    def to_dict(self, get_converted: bool = True) -> Dict:
        return {
            'md': self.safe_round(self.convert_z(value=self.md, measure_units=self.measure_units))
            if get_converted
            else self.md,
            'value': self.value,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])


class LogPointRepository(list):
    def __init__(self, objects: List[LogPoint] = None):
        if objects is None:
            objects = []

        super().__init__(objects)

    def to_dict(self, get_converted: bool = True) -> DataList:
        return [object_.to_dict(get_converted) for object_ in self]

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame(self.to_dict(get_converted))
