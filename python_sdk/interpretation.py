from typing import TypedDict

from pandas import DataFrame

from python_sdk.base import BaseObject, DataFrameable


class TypeInterpretation(TypedDict):
    meta: DataFrame
    horizons: DataFrame
    segments: DataFrame


class Interpretation(BaseObject, DataFrameable):
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

    def to_df(self) -> TypeInterpretation:
        data = self._get_data()

        return {
            'meta': DataFrame([data['meta']]),
            'horizons': DataFrame(data['horizons']).transpose(),
            'segments': DataFrame(data['segments'])
        }

    def _get_data(self):
        assembled_segments = self._papi_client.fetch_well_interpretation_assembled_segments(
            interpretation_id=self.uuid
        )
        horizons = self._request_all_pages(
            func=self._papi_client.fetch_well_interpretation_horizons,
            interpretation_id=self.uuid
        )

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
            'horizons': self._parse_papi_dict(assembled_segments['horizons']),
            'segments': self._parse_papi_dict(assembled_segments['segments']),
        }
