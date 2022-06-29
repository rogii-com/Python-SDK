from typing import Dict, List

from pandas import DataFrame

from python_sdk.base import ComplexObject, DataFrameable, ObjectRepository
from python_sdk.well import Well


class Project(ComplexObject, DataFrameable):
    def __init__(self, papi_client, **kwargs):
        super().__init__(papi_client)

        self.uuid = None
        self.name = None
        self.measure_unit = None
        self.role = None
        self.accessed_on = None
        self.modified_on = None

        self.__dict__.update(kwargs)

        self._wells_data: List[Dict] = []
        self._wells: ObjectRepository[Well] = ObjectRepository(dicts=[], objects=[])

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'measure_unit': self.measure_unit,
            'role': self.role,
            'accessed_on': self.accessed_on,
            'modified_on': self.modified_on,
        }

    def to_df(self):
        return DataFrame([self.to_dict()])

    @property
    def wells_data(self) -> List[Dict]:
        if not self._wells_data:
            self._wells_data = [
                self._parse_papi_data(well)
                for well in self._request_all_pages_with_content(
                    func=self._papi_client.fetch_project_wells,
                    project_id=self.uuid
                )
            ]

        return self._wells_data

    @property
    def wells(self) -> ObjectRepository[Well]:
        if not self._wells:
            self._wells = ObjectRepository(
                dicts=self.wells_data,
                objects=[Well(papi_client=self._papi_client, **item) for item in self.wells_data]
            )

        return self._wells
