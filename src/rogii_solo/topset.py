from typing import Any, Dict, Optional, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import BaseObject, ComplexObject, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.papi.types import PapiStarredTops
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

        self._starred_tops_data: Optional[PapiStarredTops] = None
        self._starred_top_top: Optional[Top] = None
        self._starred_top_center: Optional[Top] = None
        self._starred_top_bottom: Optional[Top] = None

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
                    Top(topset=self, **item)
                    for item in self._get_tops_data()
                ]
            )

        return self._tops

    @property
    def starred_top_top(self):
        if self._starred_top_top is None:
            starred_tops_data = self._get_starred_tops_data()
            self._starred_top_top = self.tops.find_by_id(starred_tops_data['top'])

        return self._starred_top_top

    @property
    def starred_top_center(self):
        if self._starred_top_center is None:
            starred_tops_data = self._get_starred_tops_data()
            self._starred_top_center = self.tops.find_by_id(starred_tops_data['center'])

        return self._starred_top_center

    @property
    def starred_top_bottom(self):
        if self._starred_top_bottom is None:
            starred_tops_data = self._get_starred_tops_data()
            self._starred_top_bottom = self.tops.find_by_id(starred_tops_data['bottom'])

        return self._starred_top_bottom

    def create_top(self, top_name: str, md: float):
        self._papi_client.create_topset_top(
            topset_id=self.uuid,
            top_name=top_name,
            md=self._papi_client.prepare_papi_var(md)
        )

        self._tops_data = None
        self._tops = None

    def _get_tops_data(self) -> Optional[DataList]:
        if self._tops_data is None:
            self._tops_data = self._papi_client.get_topset_tops_data(topset_id=self.uuid)

        return self._tops_data

    def _get_starred_tops_data(self):
        if self._starred_tops_data is None:
            self._starred_tops_data = self._papi_client.get_topset_starred_tops(self.uuid)

        return self._starred_tops_data


class Top(BaseObject):
    def __init__(self, topset: Topset, **kwargs):
        self.topset = topset
        self.measure_units = topset.well.project.measure_unit

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
