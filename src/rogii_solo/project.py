from typing import Any, Dict

from pandas import DataFrame

from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList
from rogii_solo.well import Typewell, Well


class Project(ComplexObject):
    def __init__(self, papi_client: PapiClient, **kwargs):
        super().__init__(papi_client)

        self.uuid = None
        self.name = None
        self.measure_unit = None
        self.role = None
        self.geo_crs = None
        self.accessed_on = None
        self.modified_on = None
        self.parent_uuid = None
        self.parent_name = None
        self.virtual = None

        self.__dict__.update(kwargs)

        self._wells_data: DataList = []
        self._wells: ObjectRepository[Well] = ObjectRepository()

        self._typewells_data: DataList = []
        self._typewells: ObjectRepository[Typewell] = ObjectRepository()

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {
            'uuid': self.uuid,
            'name': self.name,
            'measure_unit': self.measure_unit,
            'role': self.role,
            'geo_crs': self.geo_crs,
            'accessed_on': self.accessed_on,
            'modified_on': self.modified_on,
            'parent_uuid': self.parent_uuid,
            'parent_name': self.parent_name,
            'virtual': self.virtual,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])

    @property
    def wells_data(self) -> DataList:
        if not self._wells_data:
            self._wells_data = self._papi_client.get_project_wells_data(project_id=self.uuid)

        return self._wells_data

    @property
    def wells(self) -> ObjectRepository[Well]:
        if not self._wells:
            self._wells = ObjectRepository(
                dicts=self.wells_data,
                objects=[Well(papi_client=self._papi_client, project=self, **item) for item in self.wells_data]
            )

        return self._wells

    @property
    def typewells_data(self) -> DataList:
        if not self._typewells_data:
            self._typewells_data = self._papi_client._get_project_typewells_data(project_id=self.uuid)

        return self._typewells_data

    @property
    def typewells(self) -> ObjectRepository[Typewell]:
        if not self._typewells:
            self._typewells = ObjectRepository(
                dicts=self.typewells_data,
                objects=[Typewell(papi_client=self._papi_client, project=self, **item) for item in self.typewells_data]
            )

        return self._typewells
