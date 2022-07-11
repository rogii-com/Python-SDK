from pandas import DataFrame

from rogii_solo.base import ComplexObject
from rogii_solo.types import Interpretation as InterpretationType


class Interpretation(ComplexObject):
    def __init__(self, papi_client, **kwargs):
        super().__init__(papi_client)

        self.uuid = None
        self.name = None
        self.mode = None
        self.owner = None
        self.properties = None

        self.__dict__.update(kwargs)

    def to_dict(self):
        return self._get_data()

    def to_df(self) -> InterpretationType:
        data = self._get_data()

        return {
            'meta': DataFrame([data['meta']]),
            'horizons': DataFrame(data['horizons']).transpose(),
            'segments': DataFrame(data['segments']),
        }

    def _get_data(self):
        assembled_segments = self._papi_client._get_interpretation_assembled_segments_data(interpretation_id=self.uuid)
        horizons = self._papi_client._get_interpretation_horizons_data(interpretation_id=self.uuid)

        for horizon in horizons:
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
