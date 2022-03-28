from typing import Optional, NamedTuple


class SettingsAuth(NamedTuple):
    client_id: str
    client_secret: str
    solo_username: str
    solo_password: str
    papi_domain_name: str


