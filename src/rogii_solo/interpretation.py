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

        self._horizons_data: Optional[DataList] = None
        self._horizons: Optional[ObjectRepository[Horizon]] = None

        self._starred_horizons: Optional[Dict[str, str]] = None

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return self._get_data()

    def to_df(self, get_converted: bool = True) -> InterpretationType:
        data = self._get_data()

        return {
            'meta': DataFrame([data['meta']]),
            'horizons': DataFrame(data['horizons']).transpose(),
            'segments': DataFrame(data['segments']),
        }

    @property
    def horizons_data(self) -> DataList:
        if self._horizons_data is None:
            self._horizons_data = self._papi_client.get_interpretation_horizons_data(interpretation_id=self.uuid)

        return self._horizons_data

    @property
    def horizons(self) -> ObjectRepository[Horizon]:
        if self._horizons is None:
            self._horizons = ObjectRepository(
                objects=[Horizon(interpretation=self, **item) for item in self.horizons_data]
            )

        return self._horizons

    @property
    def assembled_segments_data(self) -> PapiAssembledSegments:
        if self._assembled_segments_data is None:
            self._assembled_segments_data = self._papi_client.get_interpretation_assembled_segments_data(
                interpretation_id=self.uuid
            )

        return self._assembled_segments_data

    def _get_data(self):
        assembled_segments = self.assembled_segments_data

        for horizon in self.horizons_data:
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

    @property
    def starred_horizon_top(self):
        if self._starred_horizons is None:
            self._starred_horizons = self._papi_client.get_interpretation_starred_horizons(self.uuid)

        return self._starred_horizons['top']

    @property
    def starred_horizon_center(self):
        if self._starred_horizons is None:
            self._starred_horizons = self._papi_client.get_interpretation_starred_horizons(self.uuid)

        return self._starred_horizons['center']

    @property
    def starred_horizon_bottom(self):
        if self._starred_horizons is None:
            self._starred_horizons = self._papi_client.get_interpretation_starred_horizons(self.uuid)

        return self._starred_horizons['bottom']
