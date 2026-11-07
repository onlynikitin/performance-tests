"""HTTP API-клиент выпуска карт через http-gateway."""

from typing import TypedDict

from httpx import Response

from clients.http.client import HTTPClient


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

