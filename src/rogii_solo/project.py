from typing import Any, Dict, Optional

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

        self._wells_data: Optional[DataList] = None
        self._wells: Optional[ObjectRepository[Well]] = None

        self._typewells_data: Optional[DataList] = None
        self._typewells: Optional[ObjectRepository[Well]] = None

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

    @property
    def typewells(self) -> ObjectRepository[Typewell]:
        if self._typewells is None:
            self._typewells = ObjectRepository(
                objects=[
                    Typewell(papi_client=self._papi_client, project=self, **item)
                    for item in self._get_typewells_data()
                ]
            )

        return self._typewells

    def create_well(self,
                    well_name: str,
                    operator: str,
                    api: str,
                    convergence: float,
                    azimuth: float,
                    kb: float,
                    tie_in_tvd: float,
                    tie_in_ns: float,
                    tie_in_ew: float,
                    xsrf_real: float,
                    ysrf_real: float,
                    ):
        result = self._papi_client.create_well(
            project_id=self.uuid,
            well_name=well_name,
            operator=operator,
            api=api,
            convergence=self._papi_client.prepare_papi_var(convergence),
            azimuth=self._papi_client.prepare_papi_var(azimuth),
            kb=self._papi_client.prepare_papi_var(kb),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew),
            xsrf_real=self._papi_client.prepare_papi_var(xsrf_real),
            ysrf_real=self._papi_client.prepare_papi_var(ysrf_real)
        )

        self._wells_data = None
        self._wells = None

        return result

    def create_typewell(self,
                        typewell_name: str,
                        operator: str,
                        api: str,
                        convergence: float,
                        kb: float,
                        tie_in_tvd: float,
                        tie_in_ns: float,
                        tie_in_ew: float,
                        xsrf_real: float,
                        ysrf_real: float,
                        ):
        result = self._papi_client.create_typewell(
            project_id=self.uuid,
            typewell_name=typewell_name,
            operator=operator,
            api=api,
            convergence=self._papi_client.prepare_papi_var(convergence),
            kb=self._papi_client.prepare_papi_var(kb),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew),
            xsrf_real=self._papi_client.prepare_papi_var(xsrf_real),
            ysrf_real=self._papi_client.prepare_papi_var(ysrf_real)
        )

        self._typewells_data = None
        self._typewells = None

        return result

    def _get_wells_data(self) -> DataList:
        if self._wells_data is None:
            self._wells_data = self._papi_client.get_project_wells_data(project_id=self.uuid)

        return self._wells_data

    def _get_typewells_data(self) -> DataList:
        if self._typewells_data is None:
            self._typewells_data = self._papi_client.get_project_typewells_data(project_id=self.uuid)

        return self._typewells_data
