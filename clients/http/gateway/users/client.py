from httpx import Response
from locust.env import Environment  # Импорт окружения Locust

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.client import (
    build_gateway_http_client,
    build_gateway_locust_http_client  # Импорт билдера для нагрузочного тестирования
)
from clients.http.gateway.users.schema import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)


class UsersGatewayHTTPClient(HTTPClient):
    """Клиент для /api/v1/users сервиса http-gateway."""

    def get_user_api(self, user_id: str) -> Response:
        """Получить пользователя по ID.

        :param user_id: Идентификатор пользователя.
        :return: Полный ответ httpx.Response.
        """
        return self.get(
            f"/api/v1/users/{user_id}",
            extensions=HTTPClientExtensions(route="/api/v1/users/{user_id}")  # Явно передаём логическое имя маршрута
        )


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
        request = CreateUserRequestSchema()
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """Создать клиент пользователей с общими настройками Gateway."""
    return UsersGatewayHTTPClient(client=build_gateway_http_client())


# Новый билдер для нагрузочного тестирования
def build_users_gateway_locust_http_client(environment: Environment) -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр UsersGatewayHTTPClient с хуками сбора метрик.
    """
    return UsersGatewayHTTPClient(client=build_gateway_locust_http_client(environment))