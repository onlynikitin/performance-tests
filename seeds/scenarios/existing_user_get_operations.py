"""Сидинг для сценария existing_user_get_operations."""

from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedAccountsPlan, SeedsPlan, SeedUsersPlan, SeedOperationsPlan


class ExistingUserGetOperationsSeedsScenario(SeedsScenario):
    """Подготовить 300 пользователей с кредитными счетами и историей операций."""

    @property
    def plan(self) -> SeedsPlan:
        """Вернуть план подготовки пользователей и связанных сущностей."""
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,
                credit_card_accounts=SeedAccountsPlan(
                    count=1,
                    top_up_operations=SeedOperationsPlan(count=1),
                    purchase_operations=SeedOperationsPlan(count=5),
                    cash_withdrawal_operations=SeedOperationsPlan(count=1),
                ),
            )
        )

    @property
    def scenario(self) -> str:
        """Вернуть имя сценария для сохранения и загрузки JSON."""
        return "existing_user_get_operations"


if __name__ == "__main__":
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()
