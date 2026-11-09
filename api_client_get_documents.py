"""Создать пользователя и кредитный счёт, затем получить документы счёта."""

from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.documents.client import build_documents_gateway_http_client
from clients.http.gateway.users.client import build_users_gateway_http_client


users_gateway_client = build_users_gateway_http_client()
accounts_gateway_client = build_accounts_gateway_http_client()
documents_gateway_client = build_documents_gateway_http_client()

try:
    # Создаём пользователя.
    create_user_response = users_gateway_client.create_user()
    print("Create user response:", create_user_response)

    # Открываем кредитный счёт для созданного пользователя.
    open_credit_card_account_response = accounts_gateway_client.open_credit_card_account(
        user_id=create_user_response.user.id
    )
    print("Open credit card account response:", open_credit_card_account_response)

    # Получаем тариф и контракт по ID нового счёта.
    get_tariff_document_response = documents_gateway_client.get_tariff_document(
        account_id=open_credit_card_account_response.account.id
    )
    print("Get tariff document response:", get_tariff_document_response)

    get_contract_document_response = documents_gateway_client.get_contract_document(
        account_id=open_credit_card_account_response.account.id
    )
    print("Get contract document response:", get_contract_document_response)
finally:
    users_gateway_client.client.close()
    accounts_gateway_client.client.close()
    documents_gateway_client.client.close()
