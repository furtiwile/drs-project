import requests
from urllib.parse import urljoin
from typing import Any

class GatewayClient:
    def __init__(self, base_url: str, version: str, headers: dict[str, str] | None = None) -> None:
        self.base_url = base_url
        self.version = version
        self.session = requests.Session()
        default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)
        self.session.headers.update(default_headers)
    
    def request(self, path: str, method: str = "GET", **kwargs: Any) -> requests.Response:
        url = urljoin(self.base_url, f"{self.version}{path}")
        response = self.session.request(method=method.upper(), url=url, **kwargs)
        #response.raise_for_status()
        return response
    
    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request(path, method="GET", **kwargs)
    
    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request(path, method="POST", **kwargs)
    
    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request(path, method="PUT", **kwargs)
    
    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request(path, method="PATCH", **kwargs)
    
    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request(path, method="DELETE", **kwargs)