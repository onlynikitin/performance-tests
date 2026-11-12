"""Нагрузка на открытие дебетовых счетов через HTTP API-клиенты."""

from locust import User, between, task

from clients.http.gateway.accounts.client import (
    AccountsGatewayHTTPClient,
    build_accounts_gateway_locust_http_client,
)
from clients.http.gateway.users.client import (
    UsersGatewayHTTPClient,
    build_users_gateway_locust_http_client,
)
from clients.http.gateway.users.schema import CreateUserResponseSchema


class OpenDebitCardAccountScenarioUser(User):
    """Создать пользователя один раз и многократно открывать ему счета."""

    # Сохранено по условию задания; реальный base_url задан в HTTPX-билдере.
    host = "localhost"
    wait_time = between(1, 3)

    users_gateway_client: UsersGatewayHTTPClient # Здесь будет клиент пользователей
    accounts_gateway_client: AccountsGatewayHTTPClient # Здесь будет клиент счетов
    create_user_response: CreateUserResponseSchema # Здесь будет модель ответа создания пользователя

    def on_start(self) -> None:
        """Подключить клиенты к метрикам текущего запуска и создать пользователя."""
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.environment)
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self) -> None:
        """Открыть новый дебетовый счёт для сохранённого пользователя."""
        self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )

    def on_stop(self) -> None:
        """Закрыть созданные HTTPX-клиенты при остановке пользователя Locust."""
        for attribute in ("users_gateway_client", "accounts_gateway_client"):
            api_client = getattr(self, attribute, None)
            if api_client is not None:
                api_client.client.close()
