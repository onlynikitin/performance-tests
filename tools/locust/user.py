"""Общие настройки виртуальных пользователей нагрузочных сценариев."""

from locust import User, between


class LocustBaseUser(User):
    """Базовый пользователь с общей паузой; напрямую не запускается.

    Конкретный сценарий наследует настройки и указывает собственные tasks.
    Адрес сервиса задаётся в билдере API-клиента, а не в host.
    """

    host: str = "localhost"
    abstract = True
    wait_time = between(1, 3)
