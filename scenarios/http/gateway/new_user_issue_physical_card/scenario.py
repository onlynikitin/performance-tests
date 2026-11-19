"""Новый пользователь: регистрация, дебетовый счёт и дополнительная физическая карта."""

from locust import task

from clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from clients.http.gateway.cards.schema import IssuePhysicalCardResponseSchema
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from tools.locust.user import LocustBaseUser


class IssuePhysicalCardSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    """Выполнять три связанных шага последовательно, сохраняя ответы текущего цикла."""

    create_user_response: CreateUserResponseSchema | None = None
    open_debit_card_account_response: OpenDebitCardAccountResponseSchema | None = None
    issue_physical_card_response: IssuePhysicalCardResponseSchema | None = None

    @task
    def create_user(self) -> None:
        """Очистить состояние прошлого цикла и зарегистрировать пользователя."""
        self.create_user_response = None
        self.open_debit_card_account_response = None
        self.issue_physical_card_response = None
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self) -> None:
        """Открыть счёт для пользователя, созданного в текущем цикле."""
        if self.create_user_response is None:
            return
        self.open_debit_card_account_response = (
            self.accounts_gateway_client.open_debit_card_account(
                user_id=self.create_user_response.user.id
            )
        )

    @task
    def issue_physical_card(self) -> None:
        """Выпустить дополнительную физическую карту для текущего пользователя и счёта."""
        if self.create_user_response is None or self.open_debit_card_account_response is None:
            return
        self.issue_physical_card_response = self.cards_gateway_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_debit_card_account_response.account.id,
        )

    def on_stop(self) -> None:
        """Закрыть HTTP-клиенты, подготовленные базовым TaskSet."""
        for attribute in (
            "users_gateway_client",
            "accounts_gateway_client",
            "cards_gateway_client",
            "documents_gateway_client",
            "operations_gateway_client",
        ):
            api_client = getattr(self, attribute, None)
            if api_client is not None:
                api_client.client.close()


class IssuePhysicalCardScenarioUser(LocustBaseUser):
    """Виртуальный пользователь с последовательным сценарием выпуска карты."""

    tasks = [IssuePhysicalCardSequentialTaskSet]
