from pydantic_settings import BaseSettings, SettingsConfigDict

from tools.config.grpc import GRPCClientConfig
from tools.config.http import HTTPClientConfig
from tools.config.locust import LocustUserConfig


class Settings(BaseSettings):
    """Единая конфигурация из окружения и .env в рабочем каталоге."""

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    locust_user: LocustUserConfig
    gateway_http_client: HTTPClientConfig
    gateway_grpc_client: GRPCClientConfig


settings = Settings()
