"""Создать пользователя и открыть дебетовый счёт через gRPC Gateway."""

import grpc

from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import (
    AccountsGatewayServiceStub,
)
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import (
    OpenDebitCardAccountRequest,
    OpenDebitCardAccountResponse,
)
from contracts.services.gateway.users.rpc_create_user_pb2 import (
    CreateUserRequest,
    CreateUserResponse,
)
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import (
    UsersGatewayServiceStub,
)
from tools.fakers import fake


# Один канал для обоих логических сервисов. После выполнения он закроется.
with grpc.insecure_channel("localhost:9003") as channel:
    users_gateway_service = UsersGatewayServiceStub(channel)
    accounts_gateway_service = AccountsGatewayServiceStub(channel)

    # Подготавливаем и отправляем запрос создания пользователя.
    create_user_request = CreateUserRequest(
        email=fake.email(),
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        middle_name=fake.middle_name(),
        phone_number=fake.phone_number(),
    )
    create_user_response: CreateUserResponse = users_gateway_service.CreateUser(
        create_user_request, timeout=10
    )
    print("Create user response:", create_user_response)

    # Открываем счёт для пользователя, чей ID получили в предыдущем ответе.
    open_debit_card_account_request = OpenDebitCardAccountRequest(
        user_id=create_user_response.user.id
    )
    open_debit_card_account_response: OpenDebitCardAccountResponse = (
        accounts_gateway_service.OpenDebitCardAccount(
            open_debit_card_account_request, timeout=10
        )
    )
    print("Open debit card account response:", open_debit_card_account_response)
