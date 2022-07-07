import base64
import hashlib
import uuid
from typing import Any
from urllib.parse import urljoin

from rogii_solo import __version__
from rogii_solo.papi.base import PapiClient as SdkPapiClient
from rogii_solo.papi.types import PapiVar, SettingsAuth
from rogii_solo.utils.constants import PYTHON_SDK_APP_ID, SOLO_OPEN_AUTH_SERVICE_URL, SOLO_PAPI_URL


class PapiClient(SdkPapiClient):
    def __init__(self, settings_auth: SettingsAuth):
        app_id = base64.standard_b64encode(PYTHON_SDK_APP_ID.encode()).decode()

        FINGERPRINT = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
        headers = {
            'User-Agent': f'PythonSDK/{__version__}',
            'X-Solo-Hid': f'{FINGERPRINT}:{app_id}',
        }

        papi_url = urljoin(settings_auth.papi_domain_name, SOLO_PAPI_URL)
        papi_auth_url = urljoin(settings_auth.papi_domain_name, SOLO_OPEN_AUTH_SERVICE_URL)

        super().__init__(
            papi_url=papi_url,
            papi_auth_url=papi_auth_url,
            papi_client_id=settings_auth.client_id,
            papi_client_secret=settings_auth.client_secret,
            headers=headers
        )

    def _prepare_papi_var(self, value: float) -> PapiVar:
        """
        Create value dict for PAPI
        :param value:
        :return:
        """
        if value is None:
            return {'undefined': True}

        return {'val': value}

    def _parse_papi_data(self, data: Any, default: Any = None) -> Any:
        """
        Recursive dictionary parsing.
        Elements can be either of the regular type values, list/dict, or dicts with "val" or "undefined" key.
        """
        if isinstance(data, dict):
            if 'val' in data or 'undefined' in data:
                return data.get('val', default)
            else:
                return {item: self._parse_papi_data(value) for item, value in data.items()}
        elif isinstance(data, list):
            return [self._parse_papi_data(item) for item in data]
        else:
            return data

    def _fetch_all_pages(self, func, **kwargs):
        """
        Retrieve all pages' data
        :param func:
        :param kwargs:
        :return:
        """
        result = []
        offset = self.DEFAULT_OFFSET
        last = False

        while not last:
            response = func(offset=offset, **kwargs)

            result.extend(response['content'])
            offset += self.DEFAULT_LIMIT
            last = response['last']

        return result
