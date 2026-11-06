from clients.http.client import HTTPClient
from httpx import Response

class CreateUserRequestDict(TypedDict):
    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str


class UsersGatewayHTTPClient(HTTPClient):
    def get_user_api(self, user_id):
        return self.get(f"/api/v1/users/{user_id}")

    def create_user_api(self, request: dict[str, str]) -> Response:
        return self.post("/api/v1/users", json=request)