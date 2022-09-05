from typing import Any, Dict, Optional, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ComplexObject, ObjectRepository
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList

WellType = Union[
    'rogii_solo.well.Well',
    'rogii_solo.well.Typewell',
    'rogii_solo.well.NestedWell'
]


class Topset(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: WellType, **kwargs):
        super().__init__(papi_client)

        self.well = well

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

        self._tops_data: Optional[DataList] = None
        self._tops: Optional[ObjectRepository[Top]] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'name': self.name
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict()])

    @property
    def tops(self) -> ObjectRepository['Top']:
        if self._tops is None:
            self._tops = ObjectRepository(
                objects=[
                    Top(measure_units=self.well.project.measure_unit, topset=self, **item)
                    for item in self._get_tops_data()
                ]
            )

        return self._tops

    def _get_tops_data(self) -> Optional[DataList]:
        if self._tops_data is None:
            self._tops_data = self._papi_client.get_topset_tops_data(topset_id=self.uuid)

        return self._tops_data

    def create_top(self,
                   top_name: str,
                   md: float
                   ):
        self._papi_client.create_topset_top(
            topset_id=self.uuid,
            top_name=top_name,
            md=self._papi_client.prepare_papi_var(md)
        )


class Top(BaseObject):
    def __init__(self, measure_units: EMeasureUnits, topset: Topset, **kwargs):
        self.measure_units = measure_units

        self.topset = topset

        self.uuid = None
        self.name = None
        self.md = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'name': self.name,
            'md': self.convert_z(self.md, measure_units=self.measure_units) if get_converted else self.md,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict()])
