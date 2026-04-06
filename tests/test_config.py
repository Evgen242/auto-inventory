"""Тестовая конфигурация"""
import tempfile
import os


class TestConfig:
    """Конфигурация для тестов"""

    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"

    # Используем временную БД в памяти
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Отключаем аутентификацию для тестов
    LOGIN_DISABLED = False
