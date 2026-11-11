"""Учебный сценарий работы с готовыми gRPC API-клиентами."""
from contextlib import ExitStack

from clients.grpc.gateway.users.client import build_users_gateway_grpc_client
from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.documents.client import build_documents_gateway_grpc_client


def main() -> None:
    """Создать пользователя, открыть счёт и выполнить связанные запросы."""
    with ExitStack() as stack:
        users_gateway_client = build_users_gateway_grpc_client()
        stack.callback(users_gateway_client.channel.close)
        accounts_gateway_client = build_accounts_gateway_grpc_client()
        stack.callback(accounts_gateway_client.channel.close)
        documents_gateway_client = build_documents_gateway_grpc_client()
        stack.callback(documents_gateway_client.channel.close)

        create_user_response = users_gateway_client.create_user()
        print('Create user response:', create_user_response)

        open_credit_card_account_response = accounts_gateway_client.open_credit_card_account(
            user_id=create_user_response.user.id
        )
        print('Open credit card account response:', open_credit_card_account_response)

        get_tariff_document_response = documents_gateway_client.get_tariff_document(
            account_id=open_credit_card_account_response.account.id
        )
        print('Get tariff document response:', get_tariff_document_response)

        get_contract_document_response = documents_gateway_client.get_contract_document(
            account_id=open_credit_card_account_response.account.id
        )
        print('Get contract document response:', get_contract_document_response)


if __name__ == '__main__':
    main()
