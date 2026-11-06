from httpx import Client, URL, Response, QueryParams
from typing import Any

class HTTPClient:
    def __init__(self, client: Client):
        self.client = client

    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        return self.client.get(url, params=params)

    def post(self, url: URL | str, json: Any| None = None) -> Response:
        return self.client.post(url, json=json)