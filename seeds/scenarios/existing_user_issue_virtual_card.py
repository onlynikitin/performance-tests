"""Сидинг для сценария existing_user_issue_virtual_card."""

from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedAccountsPlan, SeedsPlan, SeedUsersPlan


class ExistingUserIssueVirtualCardSeedsScenario(SeedsScenario):
    """Подготовить 300 пользователей с дебетовыми счетами для выпуска карт."""

    @property
    def plan(self) -> SeedsPlan:
        """Вернуть план подготовки пользователей и связанных сущностей."""
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,
                debit_card_accounts=SeedAccountsPlan(count=1),
            )
        )

    @property
    def scenario(self) -> str:
        """Вернуть имя сценария для сохранения и загрузки JSON."""
        return "existing_user_issue_virtual_card"


if __name__ == "__main__":
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()
