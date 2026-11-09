from pydantic import BaseModel, HttpUrl


class DocumentSchema(BaseModel):
    """Описание структуры документа."""

    url: HttpUrl
    document: str


class GetTariffDocumentResponseSchema(BaseModel):
    """Ответ получения документа тарифа."""

    tariff: DocumentSchema


class GetContractDocumentResponseSchema(BaseModel):
    """Ответ получения документа контракта."""

    contract: DocumentSchema
