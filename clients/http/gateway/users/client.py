import time

from httpx import Response

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.users.schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
)


class UsersGatewayHTTPClient(HTTPClient):
    """Клиент для /api/v1/users сервиса http-gateway."""

    def get_user_api(self, user_id: str) -> Response:
        """Получить пользователя по ID.

        :param user_id: Идентификатор пользователя.
        :return: Полный ответ httpx.Response.
        """
        return self.get(f"/api/v1/users/{user_id}")

    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """Отправить запрос создания пользователя.

        :param request: Модель данных нового пользователя.
        :return: Полный ответ httpx.Response.
        """
        return self.post("/api/v1/users", json=request.model_dump(by_alias=True))

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        """Получить и проверить данные пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Модель ответа получения пользователя.
        """
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    def create_user(self) -> CreateUserResponseSchema:
        """Подготовить данные, создать пользователя и проверить ответ.

        :return: Модель ответа создания пользователя.
        """
        request = CreateUserRequestSchema(
            email=f"user.{time.time()}@example.com",
            last_name="string",
            first_name="string",
            middle_name="string",
            phone_number="string",
        )
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """Создать клиент пользователей с общими настройками Gateway."""
    return UsersGatewayHTTPClient(client=build_gateway_http_client())
