from typing import Any, Dict, Optional

from pandas import DataFrame

from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.papi.client import PapiClient
from rogii_solo.utils.objects import find_by_uuid
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

        self._wells: Optional[ObjectRepository[Well]] = None
        self._typewells: Optional[ObjectRepository[Typewell]] = None

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
                objects=[
                    Well(papi_client=self._papi_client, project=self, **item)
                    for item in self._papi_client.get_project_wells_data(project_id=self.uuid)
                ]
            )

        return self._wells

    @property
    def typewells(self) -> ObjectRepository[Typewell]:
        if self._typewells is None:
            self._typewells = ObjectRepository(
                objects=[
                    Typewell(papi_client=self._papi_client, project=self, **item)
                    for item in self._papi_client.get_project_typewells_data(project_id=self.uuid)
                ]
            )

        return self._typewells

    def create_well(
        self,
        name: str,
        api: str,
        operator: str,
        convergence: float,
        azimuth: float,
        kb: float,
        tie_in_tvd: float,
        tie_in_ns: float,
        tie_in_ew: float,
        xsrf_real: float,
        ysrf_real: float,
    ):
        well_id = self._papi_client.create_well(
            project_id=self.uuid,
            name=name,
            operator=operator,
            api=api,
            convergence=self._papi_client.prepare_papi_var(convergence),
            azimuth=self._papi_client.prepare_papi_var(azimuth),
            kb=self._papi_client.prepare_papi_var(kb),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew),
            xsrf_real=self._papi_client.prepare_papi_var(xsrf_real),
            ysrf_real=self._papi_client.prepare_papi_var(ysrf_real),
        )
        well_data = self._papi_client.get_project_well_data(well_id=well_id['uuid'])

        if self._wells is not None:
            self._wells.append(Well(papi_client=self._papi_client, project=self, **well_data))

    def create_typewell(
        self,
        name: str,
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
        typewell_id = self._papi_client.create_typewell(
            project_id=self.uuid,
            name=name,
            operator=operator,
            api=api,
            convergence=self._papi_client.prepare_papi_var(convergence),
            kb=self._papi_client.prepare_papi_var(kb),
            tie_in_tvd=self._papi_client.prepare_papi_var(tie_in_tvd),
            tie_in_ns=self._papi_client.prepare_papi_var(tie_in_ns),
            tie_in_ew=self._papi_client.prepare_papi_var(tie_in_ew),
            xsrf_real=self._papi_client.prepare_papi_var(xsrf_real),
            ysrf_real=self._papi_client.prepare_papi_var(ysrf_real),
        )
        # No raw method for typewell
        typewell_data = find_by_uuid(
            value=typewell_id['uuid'],
            input_list=self._papi_client.get_project_typewells_data(project_id=self.uuid, query=name),
        )

        if self._typewells is not None:
            self._typewells.append(Typewell(papi_client=self._papi_client, project=self, **typewell_data))
