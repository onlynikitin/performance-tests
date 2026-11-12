from grpc import Channel
from locust.env import Environment

from clients.grpc.client import GRPCClient
from clients.grpc.gateway.client import (
    build_gateway_grpc_client,
    build_gateway_locust_grpc_client
)

from contracts.services.gateway.cards.cards_gateway_service_pb2_grpc import (
    CardsGatewayServiceStub,
)
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import (
    IssuePhysicalCardRequest,
    IssuePhysicalCardResponse,
)
from contracts.services.gateway.cards.rpc_issue_virtual_card_pb2 import (
    IssueVirtualCardRequest,
    IssueVirtualCardResponse,
)


class CardsGatewayGRPCClient(GRPCClient):
    """gRPC-клиент для выпуска карт через CardsGatewayService."""

    def __init__(self, channel: Channel) -> None:
        """Инициализировать клиент и Stub на переданном канале.

        :param channel: gRPC-канал для подключения к CardsGatewayService.
        """
        super().__init__(channel)
        self.stub = CardsGatewayServiceStub(channel)

    def issue_virtual_card_api(
        self, request: IssueVirtualCardRequest
    ) -> IssueVirtualCardResponse:
        """Вызвать IssueVirtualCard через сгенерированный Stub.

        :param request: Сообщение с ID пользователя и счёта.
        :return: Protobuf-ответ с данными созданной виртуальной карты.
        """
        return self.stub.IssueVirtualCard(request)

    def issue_physical_card_api(
        self, request: IssuePhysicalCardRequest
    ) -> IssuePhysicalCardResponse:
        """Вызвать IssuePhysicalCard через сгенерированный Stub.

        :param request: Сообщение с ID пользователя и счёта.
        :return: Protobuf-ответ с данными созданной физической карты.
        """
        return self.stub.IssuePhysicalCard(request)

    def issue_virtual_card(
        self, user_id: str, account_id: str
    ) -> IssueVirtualCardResponse:
        """Подготовить запрос и выпустить виртуальную карту.

        :param user_id: Идентификатор пользователя.
        :param account_id: Идентификатор счёта.
        :return: Protobuf-ответ с информацией о созданной карте.
        """
        request = IssueVirtualCardRequest(user_id=user_id, account_id=account_id)
        return self.issue_virtual_card_api(request)

    def issue_physical_card(
        self, user_id: str, account_id: str
    ) -> IssuePhysicalCardResponse:
        """Подготовить запрос и выпустить физическую карту.

        :param user_id: Идентификатор пользователя.
        :param account_id: Идентификатор счёта.
        :return: Protobuf-ответ с информацией о созданной карте.
        """
        request = IssuePhysicalCardRequest(user_id=user_id, account_id=account_id)
        return self.issue_physical_card_api(request)


def build_cards_gateway_grpc_client() -> CardsGatewayGRPCClient:
    """Создать клиент карт с каналом из общего билдера Gateway.

    :return: Инициализированный CardsGatewayGRPCClient.
    """
    return CardsGatewayGRPCClient(channel=build_gateway_grpc_client())

def build_cards_gateway_locust_grpc_client(environment: Environment) -> CardsGatewayGRPCClient:
    """
    Функция создаёт экземпляр CardsGatewayGRPCClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр CardsGatewayGRPCClient с хуками сбора метрик.
    """
    return CardsGatewayGRPCClient(channel=build_gateway_locust_grpc_client(environment))
