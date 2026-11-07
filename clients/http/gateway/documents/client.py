from typing import TypedDict

from httpx import Response

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


class DocumentDict(TypedDict):
    """Описание структуры документа."""

    url: str
    document: str


class GetTariffDocumentResponseDict(TypedDict):
    """Описание ответа получения тарифа."""

    tariff: DocumentDict


class GetContractDocumentResponseDict(TypedDict):
    """Описание ответа получения контракта."""

    contract: DocumentDict


class DocumentsGatewayHTTPClient(HTTPClient):
    """Клиент для /api/v1/documents сервиса http-gateway."""

    def get_tariff_document_api(self, account_id: str) -> Response:
        """Получить тариф по счёту.

        :param account_id: Идентификатор счёта.
        :return: Объект httpx.Response.
        """
        return self.get(f"/api/v1/documents/tariff-document/{account_id}")

    def get_contract_document_api(self, account_id: str) -> Response:
        """Получить контракт по счёту.

        :param account_id: Идентификатор счёта.
        :return: Объект httpx.Response.
        """
        return self.get(f"/api/v1/documents/contract-document/{account_id}")

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseDict:
        """Получить тариф и разобрать JSON-ответ.

        :param account_id: Идентификатор счёта.
        :return: Словарь с ключом tariff и данными документа.
        """
        response = self.get_tariff_document_api(account_id)
        return response.json()

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseDict:
        """Получить контракт и разобрать JSON-ответ.

        :param account_id: Идентификатор счёта.
        :return: Словарь с ключом contract и данными документа.
        """
        response = self.get_contract_document_api(account_id)
        return response.json()


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """Создать настроенный клиент документов.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())
