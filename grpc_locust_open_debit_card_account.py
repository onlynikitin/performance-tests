"""Нагрузка на открытие дебетовых счетов через gRPC API-клиенты."""

from locust import User, between, task

from clients.grpc.gateway.accounts.client import (
    AccountsGatewayGRPCClient,
    build_accounts_gateway_locust_grpc_client,
)
from clients.grpc.gateway.users.client import (
    UsersGatewayGRPCClient,
    build_users_gateway_locust_grpc_client,
)
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class OpenDebitCardAccountScenarioUser(User):
    """Создать пользователя один раз и многократно открывать ему счета."""

    # По условию задания; реальный адрес сервера задан в билдере канала.
    host = "localhost"
    wait_time = between(1, 3)

    users_gateway_client: UsersGatewayGRPCClient
    accounts_gateway_client: AccountsGatewayGRPCClient
    create_user_response: CreateUserResponse

    def on_start(self) -> None:
        """Создать клиенты с метриками Locust и банковского пользователя."""
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_grpc_client(self.environment)
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self) -> None:
        """Открыть новый дебетовый счёт для сохранённого пользователя."""
        self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )

    def on_stop(self) -> None:
        """Закрыть созданные gRPC-каналы при остановке пользователя Locust."""
        for attribute in ("users_gateway_client", "accounts_gateway_client"):
            api_client = getattr(self, attribute, None)
            if api_client is not None:
                api_client.channel.close()
