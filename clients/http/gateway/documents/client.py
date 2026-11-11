from httpx import Response
from locust.env import Environment

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.client import (
    build_gateway_http_client,
    build_gateway_locust_http_client,
)
from clients.http.gateway.documents.schema import (
    GetTariffDocumentResponseSchema,
    GetContractDocumentResponseSchema,
)


class DocumentsGatewayHTTPClient(HTTPClient):
    """Клиент для /api/v1/documents сервиса http-gateway."""

    def get_tariff_document_api(self, account_id: str) -> Response:
        """Получить тариф по счёту.

        :param account_id: Идентификатор счёта.
        :return: Объект httpx.Response.
        """
        return self.get(
            f"/api/v1/documents/tariff-document/{account_id}",
            extensions=HTTPClientExtensions(route="/api/v1/documents/tariff-document/{account_id}")
                        )

    def get_contract_document_api(self, account_id: str) -> Response:
        """Получить контракт по счёту.

        :param account_id: Идентификатор счёта.
        :return: Объект httpx.Response.
        """
        return self.get(
            f"/api/v1/documents/contract-document/{account_id}",
            extensions = HTTPClientExtensions(route="/api/v1/documents/contract-document/{account_id}")
        )

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        """Получить тариф и разобрать JSON-ответ.

        :param account_id: Идентификатор счёта.
        :return: Модель с полем tariff и данными документа.
        """
        response = self.get_tariff_document_api(account_id)
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseSchema:
        """Получить контракт и разобрать JSON-ответ.

        :param account_id: Идентификатор счёта.
        :return: Модель с полем contract и данными документа.
        """
        response = self.get_contract_document_api(account_id)
        return GetContractDocumentResponseSchema.model_validate_json(response.text)


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """Создать настроенный клиент документов.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())


def build_documents_gateway_locust_http_client(environment: Environment) -> DocumentsGatewayHTTPClient:
    """Создать API-клиент с HTTPX-хуками сбора метрик Locust.

    :param environment: Окружение текущего запуска Locust, принимающее метрики.
    :return: DocumentsGatewayHTTPClient с настроенным HTTPX-клиентом.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))
