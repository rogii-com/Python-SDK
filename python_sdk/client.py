from typing import Optional

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


    def fetch_projects(self, project_filter: str = None):
        return self.papi_client.fetch_projects(project_filter=project_filter)
