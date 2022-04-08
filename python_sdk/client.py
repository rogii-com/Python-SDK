import pandas as pd

from .papi import PapiClient
from .utils.constants import SOLO_PAPI_DEFAULT_DOMAIN_NAME
from .utils.settings import SettingsAuth


class PyRogii:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 solo_username: str,
                 solo_password: str,
                 papi_domain_name: str = SOLO_PAPI_DEFAULT_DOMAIN_NAME
                 ):
        self.papi_client = PapiClient(
            SettingsAuth(
                client_id=client_id,
                client_secret=client_secret,
                solo_username=solo_username,
                solo_password=solo_password,
                papi_domain_name=papi_domain_name
            )
        )

    def to_pandas_dataframe(self, list) -> pd.DataFrame:
        return pd.DataFrame(list)

    def fetch_projects(self, project_filter: str = None):
        return self.papi_client.fetch_projects(project_filter=project_filter)

    def get_projects(self, project_filter: str = None) -> pd.DataFrame:
        return self.to_pandas_dataframe(self.fetch_projects(project_filter=project_filter)['content'])

    def fetch_project_wells(self, project_uuid: str,  well_filter: str = None):
        return self.papi_client.fetch_project_wells(project_uuid=project_uuid, well_filter=well_filter)

    def get_project_wells(self, project_uuid: str,  well_filter: str = None):
        data = self.papi_client.fetch_project_wells(project_uuid=project_uuid, well_filter=well_filter)
        return self.to_pandas_dataframe(data['content'])

    def fetch_well(self, well_uuid: str):
        return self.papi_client.fetch_well(well_uuid=well_uuid)

    def get_well(self, well_uuid: str):
        data = self.papi_client.fetch_well(well_uuid=well_uuid)
        return self.to_pandas_dataframe([data, ])
