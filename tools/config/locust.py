from pydantic import BaseModel


class LocustUserConfig(BaseModel):
    """Границы паузы между задачами в секундах."""

    wait_time_min: float = 1
    wait_time_max: float = 3
