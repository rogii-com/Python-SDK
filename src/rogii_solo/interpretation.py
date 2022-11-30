from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.calculations.converters import meters_to_feet
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.horizon import Horizon
from rogii_solo.papi.client import PapiClient
from rogii_solo.papi.types import PapiAssembledSegments
from rogii_solo.types import DataList
from rogii_solo.types import Interpretation as InterpretationType

TVT_DATA_MAX_MD_STEP = 100000


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
    def assembled_segments(self):
        if self._assembled_segments_data is not None:
            return {
                'horizons': self._assembled_segments_data['horizons'],
                'segments': self._assembled_segments_data['segments']
            }

        self._assembled_segments_data = self._papi_client.get_interpretation_assembled_segments_data(
            interpretation_id=self.uuid
        )

        assembled_horizons_data = self._assembled_segments_data['horizons']
        measure_units = self.well.project.measure_unit

        for horizon in self._get_horizons_data():
            assembled_horizons_data[horizon['uuid']]['name'] = horizon['name']
            if measure_units != EMeasureUnits.METER:
                assembled_horizons_data[horizon['uuid']]['tvd'] = meters_to_feet(
                    assembled_horizons_data[horizon['uuid']]['tvd']
                )

        return {
            'horizons': self._assembled_segments_data['horizons'],
            'segments': self._assembled_segments_data['segments']
        }

    def get_tvt_data(self, md_step: int = 1) -> DataList:
        return self._papi_client.get_interpretation_tvt_data(
            interpretation_id=self.uuid,
            md_step=md_step
        )

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
        meta = {
            'uuid': self.uuid,
            'name': self.name,
            'mode': self.mode,
            'owner': self.owner,
            'properties': self.properties,
        }

        return {
            'meta': meta,
            'horizons': self.assembled_segments['horizons'],
            'segments': self.assembled_segments['segments'],
        }
