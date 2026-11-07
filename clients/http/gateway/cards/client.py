"""HTTP API-клиент выпуска карт через http-gateway."""

from typing import TypedDict

from httpx import Response

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


class CardDict(TypedDict):
    """Структура карты в ответе API."""

    id: str
    pin: str
    cvv: str
    type: str
    status: str
    accountId: str
    cardNumber: str
    cardHolder: str
    expiryDate: str
    paymentSystem: str


class IssueVirtualCardRequestDict(TypedDict):
    """Структура JSON-тела выпуска виртуальной карты.

    userId: UUID пользователя в строковом представлении.
    accountId: UUID дебетового или кредитного счёта в строковом представлении.
    """

    userId: str
    accountId: str


class IssuePhysicalCardRequestDict(TypedDict):
    """Структура JSON-тела выпуска физической карты.

    userId: UUID пользователя в строковом представлении.
    accountId: UUID дебетового или кредитного счёта в строковом представлении.
    """

    userId: str
    accountId: str


class IssueVirtualCardResponseDict(TypedDict):
    """Ответ успешного выпуска виртуальной карты."""

    card: CardDict


class IssuePhysicalCardResponseDict(TypedDict):
    """Ответ успешного выпуска физической карты."""

    card: CardDict


class CardsGatewayHTTPClient(HTTPClient):
    """Клиент запросов выпуска карт через http-gateway.

    Наследует инициализацию и общие HTTP-методы класса HTTPClient.
    Для работы принимает настроенный httpx.Client через базовый __init__.
    """

    def issue_virtual_card_api(
        self,
        request: IssueVirtualCardRequestDict,
    ) -> Response:
        """Выпустите виртуальную карту для указанного счёта.

        :param request: Словарь с userId пользователя и accountId счёта
            в строковом представлении UUID.
        :return: httpx.Response с HTTP-статусом, заголовками и телом ответа.
            При успехе JSON-тело содержит объект card с данными карты.
        """
        return self.post("/api/v1/cards/issue-virtual-card", json=request)

    def issue_physical_card_api(
        self,
        request: IssuePhysicalCardRequestDict,
    ) -> Response:
        """Выпустите физическую карту для указанного счёта.

        :param request: Словарь с userId пользователя и accountId счёта
            в строковом представлении UUID.
        :return: httpx.Response с HTTP-статусом, заголовками и телом ответа.
            При успехе JSON-тело содержит объект card с данными карты.
        """
        return self.post("/api/v1/cards/issue-physical-card", json=request)


    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseDict:
        """Подготовить запрос и выпустить виртуальную карту.

        :param user_id: Идентификатор пользователя.
        :param account_id: Идентификатор счёта.
        :return: Разобранный словарь ответа с ключом card.
        """
        request = IssueVirtualCardRequestDict(userId=user_id, accountId=account_id)
        response = self.issue_virtual_card_api(request)
        return response.json()

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseDict:
        """Подготовить запрос и выпустить физическую карту.

        :param user_id: Идентификатор пользователя.
        :param account_id: Идентификатор счёта.
        :return: Разобранный словарь ответа с ключом card.
        """
        request = IssuePhysicalCardRequestDict(userId=user_id, accountId=account_id)
        response = self.issue_physical_card_api(request)
        return response.json()


# Добавляем builder для CardsGatewayHTTPClient
def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client())