"""Существующий пользователь: просмотр счетов и выпуск виртуальной карты."""

from locust import events, task
from locust.env import Environment

from clients.grpc.gateway.locust import GatewayGRPCTaskSet
from seeds.scenarios.existing_user_issue_virtual_card import (
    ExistingUserIssueVirtualCardSeedsScenario,
)
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


@events.init.add_listener
def init(environment: Environment, **kwargs) -> None:
    """Подготовить данные до нагрузки и сохранить набор в окружении Locust."""
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()
    environment.seeds = seeds_scenario.load()


class IssueVirtualCardTaskSet(GatewayGRPCTaskSet):
    """Чаще запрашивать счета и реже выпускать дополнительные виртуальные карты."""

    seed_user: SeedUserResult

    def on_start(self) -> None:
        """Создать API-клиенты и выбрать банковского пользователя из сидинга."""
        super().on_start()
        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(3)
    def get_accounts(self) -> None:
        """Получить счета выбранного пользователя."""
        self.accounts_gateway_client.get_accounts(
            user_id=self.seed_user.user_id
        )

    @task(1)
    def issue_virtual_card(self) -> None:
        """Выпустить виртуальную карту для первого дебетового счёта пользователя."""
        self.cards_gateway_client.issue_virtual_card(
            user_id=self.seed_user.user_id,
            account_id=self.seed_user.debit_card_accounts[0].account_id,
        )


class IssueVirtualCardScenarioUser(LocustBaseUser):
    """Виртуальный пользователь с набором задач выпуска карт."""

    tasks = [IssueVirtualCardTaskSet]
