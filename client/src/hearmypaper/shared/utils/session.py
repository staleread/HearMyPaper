from requests import Session
from urllib.parse import urljoin


class ApiSession(Session):
    def __init__(self, base_url=None):
        self.base_url = base_url
        super().__init__()

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)
