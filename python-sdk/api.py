from typing import Optional

class PyRogii:
    def __init__(self,
                 project_id: int,
                 client_id: int,
                 client_secret: Optional[str] = None,
                 solo_username: Optional[str] = None,
                 solo_password: Optional[str] = None
                ):
        self.project_id = project_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.solo_username = solo_username
        self.solo_password = solo_password
