from pydantic import BaseModel


class GRPCClientConfig(BaseModel):
    """Хост и порт gRPC-сервиса."""

    port: int
    host: str

    @property
    def client_url(self) -> str:
        return f"{self.host}:{self.port}"
