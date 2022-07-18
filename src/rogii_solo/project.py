from typing import Dict, List

from pandas import DataFrame

from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.well import Well


class Project(ComplexObject):
    def __init__(self, papi_client: PapiClient, **kwargs):
        super().__init__(papi_client)

        self.uuid = None
        self.name = None
        self.measure_unit = None
        self.role = None
        self.accessed_on = None
        self.modified_on = None

        self.__dict__.update(kwargs)

        self._wells_data: List[Dict] = []
        self._wells: ObjectRepository[Well] = ObjectRepository()

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
            self._wells_data = self._papi_client._get_project_wells_data(project_id=self.uuid)

        return self._wells_data

    @property
    def wells(self) -> ObjectRepository[Well]:
        if not self._wells:
            self._wells = ObjectRepository(
                dicts=self.wells_data,
                objects=[Well(papi_client=self._papi_client, project=self, **item) for item in self.wells_data]
            )

        return self._wells
