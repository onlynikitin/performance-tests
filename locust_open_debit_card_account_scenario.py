"""Нагрузочный сценарий: повторное открытие дебетовых счетов пользователю."""
from locust import HttpUser, between, task

from tools.fakers import fake


class OpenDebitCardAccountScenarioUser(HttpUser):
    """Создаёт пользователя при старте и многократно открывает ему счета."""

    wait_time = between(1, 3)
    user_data: dict

    def on_start(self) -> None:
        """Один раз создать банковского пользователя и сохранить ответ."""
        request = {
            "email": fake.email(),
            "lastName": fake.last_name(),
            "firstName": fake.first_name(),
            "middleName": fake.middle_name(),
            "phoneNumber": fake.phone_number()
        }
        response = self.client.post("/api/v1/users", json=request)
        self.user_data = response.json()

    @task
    def open_debit_card_account(self) -> None:
        """Открыть новый дебетовый счёт для сохранённого пользователя."""
        self.client.post(
            "/api/v1/accounts/open-debit-card-account",
            json={"userId": self.user_data["user"]["id"]}
        )
