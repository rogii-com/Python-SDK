import base64
import hashlib
from typing import Optional
from urllib.parse import urljoin
import uuid

from solo_connect_sdk import PapiClient as SdkPapiClient

from . import __version__
from .utils.constants import PYTHON_SDK_APP_ID, SOLO_OPEN_AUTH_SERVICE_URL, SOLO_PAPI_URL
from .utils.settings import SettingsAuth


class PapiClient(SdkPapiClient):
    def __init__(self, settings_auth: SettingsAuth):
        print('settings_auth:', settings_auth)
        app_id = base64.standard_b64encode(PYTHON_SDK_APP_ID.encode()).decode()

        FINGERPRINT = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
        headers = {
            'User-Agent': f'PythonSDK/{__version__}',
            'X-Solo-Hid': f'{FINGERPRINT}:{app_id}',
        }

        papi_url = urljoin(settings_auth.papi_domain_name, SOLO_PAPI_URL)
        papi_auth_url = urljoin(settings_auth.papi_domain_name, SOLO_OPEN_AUTH_SERVICE_URL)
        print(f'papi_url={papi_url}\n  papi_auth_url={papi_auth_url}')

        super().__init__(
            papi_url = papi_url,
            papi_auth_url = papi_auth_url,
            papi_client_id = settings_auth.client_id,
            papi_client_secret = settings_auth.client_secret,
            solo_username = settings_auth.solo_username,
            solo_password = settings_auth.solo_password,
            headers=headers
        )
