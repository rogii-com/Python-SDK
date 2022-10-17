from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.horizon import Horizon
from rogii_solo.papi.client import PapiClient
from rogii_solo.papi.types import PapiAssembledSegments
from rogii_solo.types import DataList
from rogii_solo.types import Interpretation as InterpretationType


class Interpretation(ComplexObject):
    DEFAULT_MD_STEP = 5000

    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client)

        self.well = well

        self.uuid = None
        self.name = None
        self.mode = None
        self.owner = None
        self.properties = None

        self.__dict__.update(kwargs)

        self._assembled_segments_data: Optional[PapiAssembledSegments] = None

        self._horizons_tvt_data: Optional[DataList] = None
        self._md_step: Optional[int] = None

        self._horizons_data: Optional[DataList] = None
        self._horizons: Optional[ObjectRepository[Horizon]] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return self._get_data()

    def to_df(self, get_converted: bool = True) -> InterpretationType:
        data = self._get_data()

        return {
            'meta': DataFrame([data['meta']]),
            'horizons': DataFrame(data['horizons']).transpose(),
            'segments': DataFrame(data['segments']),
        }

    def get_assembled_segments_data(self) -> PapiAssembledSegments:
        if self._assembled_segments_data is None:
            self._assembled_segments_data = self._papi_client.get_interpretation_assembled_segments_data(
                interpretation_id=self.uuid
            )

        return self._assembled_segments_data

    def get_horizons_tvt_data(self, md_step: int = DEFAULT_MD_STEP) -> DataList:
        if self._horizons_tvt_data is None or self._md_step != md_step:
            self._md_step = md_step
            self._horizons_tvt_data = self._papi_client.get_horizons_tvt_data(
                interpretation_id=self.uuid,
                md_step=md_step
            )

        return self._horizons_tvt_data

    @property
    def horizons(self) -> ObjectRepository[Horizon]:
        if self._horizons is None:
            self._horizons = ObjectRepository(
                objects=[Horizon(interpretation=self, **item) for item in self._get_horizons_data()]
            )

        return self._horizons

    def _get_horizons_data(self) -> DataList:
        if self._horizons_data is None:
            self._horizons_data = self._papi_client.get_interpretation_horizons_data(interpretation_id=self.uuid)

        return self._horizons_data

    def _get_data(self):
        assembled_segments = self.get_assembled_segments_data()

        for horizon in self._get_horizons_data():
            assembled_segments['horizons'][horizon['uuid']]['name'] = horizon['name']

        meta = {
            'uuid': self.uuid,
            'name': self.name,
            'mode': self.mode,
            'owner': self.owner,
            'properties': self.properties,
        }

        return {
            'meta': meta,
            'horizons': assembled_segments['horizons'],
            'segments': assembled_segments['segments'],
        }
