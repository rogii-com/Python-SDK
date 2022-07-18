from typing import Dict, List

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.horizon import Horizon
from rogii_solo.papi.client import PapiClient
from rogii_solo.papi.types import PapiAssembledSegments
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

        self._assembled_segments_data: PapiAssembledSegments = {}

        self._horizons_data: List[Dict] = []
        self._horizons: ObjectRepository[Horizon] = ObjectRepository()

    def to_dict(self):
        return self._get_data()

    def to_df(self) -> InterpretationType:
        data = self._get_data()

        return {
            'meta': DataFrame([data['meta']]),
            'horizons': DataFrame(data['horizons']).transpose(),
            'segments': DataFrame(data['segments']),
        }

    @property
    def horizons_data(self) -> List[Dict]:
        if not self._horizons_data:
            self._horizons_data = self._papi_client._get_interpretation_horizons_data(interpretation_id=self.uuid)

        return self._horizons_data

    @property
    def horizons(self) -> ObjectRepository[Horizon]:
        if not self._horizons:
            self._horizons = ObjectRepository(
                dicts=self.horizons_data,
                objects=[Horizon(interpretation=self, **item) for item in self.horizons_data]
            )

        return self._horizons

    @property
    def assembled_segments_data(self) -> PapiAssembledSegments:
        if not self._assembled_segments_data:
            self._assembled_segments_data = self._papi_client._get_interpretation_assembled_segments_data(
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
