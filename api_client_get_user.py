"""Создать пользователя и получить его через API-клиент с Pydantic."""

from clients.http.gateway.users.client import build_users_gateway_http_client


users_gateway_client = build_users_gateway_http_client()

try:
    create_user_response = users_gateway_client.create_user()
    print("Create user data:", create_user_response)

    get_user_response = users_gateway_client.get_user(create_user_response.user.id)
    print("Get user data:", get_user_response)
finally:
    users_gateway_client.client.close()
