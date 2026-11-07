from httpx import Client

def build_gateway_http_client() -> Client:
    return Client(timeout=100, base_url="http://localhost:8003")