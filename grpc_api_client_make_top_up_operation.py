"""Учебный сценарий работы с готовыми gRPC API-клиентами."""
from contextlib import ExitStack

from clients.grpc.gateway.users.client import build_users_gateway_grpc_client
from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.operations.client import build_operations_gateway_grpc_client


def main() -> None:
    """Создать пользователя, открыть счёт и выполнить связанные запросы."""
    with ExitStack() as stack:
        users_gateway_client = build_users_gateway_grpc_client()
        stack.callback(users_gateway_client.channel.close)
        accounts_gateway_client = build_accounts_gateway_grpc_client()
        stack.callback(accounts_gateway_client.channel.close)
        operations_gateway_client = build_operations_gateway_grpc_client()
        stack.callback(operations_gateway_client.channel.close)

        create_user_response = users_gateway_client.create_user()
        print('Create user response:', create_user_response)

        open_debit_card_account_response = accounts_gateway_client.open_debit_card_account(
            user_id=create_user_response.user.id
        )
        print('Open debit card account response:', open_debit_card_account_response)

        make_top_up_operation_response = operations_gateway_client.make_top_up_operation(
            card_id=open_debit_card_account_response.account.cards[0].id,
            account_id=open_debit_card_account_response.account.id
        )
        print('Make top up operation response:', make_top_up_operation_response)


if __name__ == '__main__':
    main()
