from typing import Any, Dict, Optional, Union

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.calculations.converters import feet_to_meters
from rogii_solo.exceptions import InvalidTopDataException
from rogii_solo.papi.client import PapiClient
from rogii_solo.papi.types import PapiStarredTops
from rogii_solo.utils.objects import find_by_uuid

WellType = Union['rogii_solo.well.Well', 'rogii_solo.well.Typewell', 'rogii_solo.well.NestedWell']


class Topset(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: WellType, **kwargs):
        super().__init__(papi_client)

        self.well = well

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

        self._tops: Optional[ObjectRepository[Top]] = None
        self._starred_tops_data: Optional[PapiStarredTops] = None
        self._starred_top_top: Optional[Top] = None
        self._starred_top_center: Optional[Top] = None
        self._starred_top_bottom: Optional[Top] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])

    @property
    def tops(self) -> ObjectRepository['Top']:
        if self._tops is None:
            self._tops = ObjectRepository(
                objects=[
                    Top(papi_client=self._papi_client, topset=self, **item)
                    for item in self._papi_client.get_topset_tops_data(topset_id=self.uuid)
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

    def create_top(self, name: str, md: float):
        if not 0 <= md <= 100000:
            raise InvalidTopDataException

        top_id = self._papi_client.create_topset_top(
            topset_id=self.uuid, name=name, md=self._papi_client.prepare_papi_var(md)
        )

        # No raw method for top
        top_data = find_by_uuid(
            value=top_id['uuid'], input_list=self._papi_client.get_topset_tops_data(topset_id=self.uuid)
        )

        if self._tops is not None:
            self._tops.append(Top(topset=self, **top_data))

    def _get_starred_tops_data(self):
        if self._starred_tops_data is None:
            self._starred_tops_data = self._papi_client.get_topset_starred_tops(self.uuid)

        return self._starred_tops_data


class Top(ComplexObject):
    def __init__(self, papi_client: PapiClient, topset: Topset, **kwargs):
        super().__init__(papi_client)

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
            # MD is returned in project units
            'md': self.md if get_converted else feet_to_meters(self.md),
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])

    def update_meta(self, name: str, md: float):
        if not 0 <= md <= 100000:
            raise InvalidTopDataException

        func_data = {
            func_param: func_arg
            for func_param, func_arg in locals().items()
            if func_arg is not None and func_param != 'self'
        }
        request_data = {key: self._papi_client.prepare_papi_var(value) for key, value in func_data.items()}

        is_updated = self._papi_client.update_top_meta(top_id=self.uuid, **request_data)

        if is_updated:
            self.__dict__.update(func_data)

        return self
