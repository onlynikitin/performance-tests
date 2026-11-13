"""Список счетов: создание пользователя, открытие депозита и чтение через HTTP."""

from locust import User, between, task

from clients.http.gateway.locust import GatewayHTTPTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema


class GetAccountsTaskSet(GatewayHTTPTaskSet):
    """Выбирать действия по весам 2:2:6, сохраняя ответ текущего пользователя."""

    create_user_response: CreateUserResponseSchema | None = None

    @task(2)
    def create_user(self) -> None:
        """Создать нового пользователя и сохранить его для следующих задач."""
        self.create_user_response = None
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self) -> None:
        """Открыть депозит только при наличии сохранённого пользователя."""
        if self.create_user_response is None:
            return
        self.accounts_gateway_client.open_deposit_account(
            user_id=self.create_user_response.user.id
        )

    @task(6)
    def get_accounts(self) -> None:
        """Получить счета текущего пользователя; без пользователя пропустить задачу."""
        if self.create_user_response is None:
            return
        self.accounts_gateway_client.get_accounts(
            user_id=self.create_user_response.user.id
        )

    def on_stop(self) -> None:
        """Закрыть клиенты, созданные базовым TaskSet."""
        for attribute in (
            "users_gateway_client",
            "cards_gateway_client",
            "accounts_gateway_client",
            "documents_gateway_client",
            "operations_gateway_client",
        ):
            api_client = getattr(self, attribute, None)
            if api_client is not None:
                api_client.client.close()


class GetAccountsScenarioUser(User):
    """Виртуальный пользователь с набором задач получения счетов."""

    # Сохранено по примеру курса; адрес задан в билдере API-клиента.
    host = "localhost"
    tasks = [GetAccountsTaskSet]
    wait_time = between(1, 3)
