from typing import Any, Dict, Optional

from pandas import DataFrame

from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList
from rogii_solo.well import Well


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

        self._wells_data: Optional[DataList] = None
        self._wells: Optional[ObjectRepository[Well]] = None

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
    def wells(self) -> ObjectRepository[Well]:
        if self._wells is None:
            self._wells = ObjectRepository(
                objects=[Well(papi_client=self._papi_client, project=self, **item) for item in self._get_wells_data()]
            )

        return self._wells

    def _get_wells_data(self) -> DataList:
        if self._wells_data is None:
            self._wells_data = self._papi_client.get_project_wells_data(project_id=self.uuid)

        return self._wells_data
