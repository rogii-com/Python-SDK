from typing import Any, Dict, Union

from pandas import DataFrame

import rogii_solo.project
from rogii_solo.base import ComplexObject
from rogii_solo.papi.client import PapiClient

WellType = Union['rogii_solo.well.Well', 'rogii_solo.well.Typewell', 'rogii_solo.well.NestedWell']


# class Top(BaseObject):
#     def __init__(self, topset: Topset, **kwargs):
#         self.topset = topset
#         self._name = None
#
#     @property
#     def name(self) -> DataList:
#         if not self._name:
#             self._horizons_data = self._papi_client.get_interpretation_horizons_data(interpretation_id=self.uuid)
#
#         return self._horizons_data

class Topset(ComplexObject):
    def __init__(self, papi_client: PapiClient, well: WellType, **kwargs):
        super().__init__(papi_client)

        self.well = well

        self.uuid = None
        self.name = None

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'name': self.name
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict()])
