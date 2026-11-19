from locust import task

from tools.locust.user import LocustBaseUser
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.accounts import OpenDebitCardAccountResponseSchema
from clients.http.gateway.cards import IssuePhysicalCardResponseSchema

class IssuePhysicalCardSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    create_user_response: CreateUserResponseSchema | None = None
    open_debit_card_account_response: OpenDebitCardAccountResponseSchema | None = None
    issue_physical_card_response: IssuePhysicalCardResponseSchema | None = None

    @task
    def create_user(self):
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        if not self.create_user_response:
            return

        self.open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user_id
    )

    @task
    def issue_physical_card(self):
        if not self.open_debit_card_account_response:
            return

        self.issue_physical_card_response = self.cards_gateway_client.issue_physical_card(
            user_id=self.open_debit_card_account_response.user.id,
            account_id=self.open_debit_card_account_response.account.id
    )

class IssuePhysicalCardSequentialTaskSet(LocustBaseUser):
    tasks = [IssuePhysicalCardSequentialTaskSet]