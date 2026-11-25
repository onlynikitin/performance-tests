"""Общие настройки виртуальных пользователей нагрузочных сценариев."""

from locust import User, between

from config import settings


class LocustBaseUser(User):
    """Базовый пользователь с общей паузой; напрямую не запускается.

    Конкретный сценарий наследует настройки и указывает собственные tasks.
    Адрес сервиса задаётся в билдере API-клиента, а не в host.
    """

    host: str = "localhost"
    abstract = True
    wait_time = between(
        min_wait=settings.locust_user.wait_time_min,
        max_wait=settings.locust_user.wait_time_max,
    )
