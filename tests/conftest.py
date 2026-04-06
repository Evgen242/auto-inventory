"""Фикстуры для pytest"""
import pytest
import os
import sys

# Добавляем корневую директорию в PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from tests.test_config import TestConfig


@pytest.fixture(scope="function")
def app():
    """Создание тестового приложения с тестовой конфигурацией"""
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Тестовый клиент"""
    return app.test_client()


@pytest.fixture(scope="function")
def app_context(app):
    """Контекст приложения"""
    with app.app_context():
        yield


@pytest.fixture(scope="function")
def test_user(app):
    """Создание тестового пользователя"""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("test123")
        db.session.add(user)
        db.session.commit()
        # Сохраняем ID для использования вне сессии
        user_id = user.id
        return user_id


@pytest.fixture(scope="function")
def authenticated_client(client, test_user, app):
    """Клиент с авторизацией"""
    with app.app_context():
        # Используем db.session.get вместо User.query.get
        user = db.session.get(User, test_user)
        client.post("/auth/login", data={"username": user.username, "password": "test123"})
    return client


@pytest.fixture(scope="function")
def admin_user(app):
    """Создание администратора"""
    with app.app_context():
        admin = User(username="admin", email="admin@example.com", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        admin_id = admin.id
        return admin_id


@pytest.fixture(scope="function")
def admin_client(client, admin_user, app):
    """Клиент с правами администратора"""
    with app.app_context():
        admin = db.session.get(User, admin_user)
        client.post("/auth/login", data={"username": admin.username, "password": "admin123"})
    return client


@pytest.fixture(scope="function")
def user_instance(app, test_user):
    """Экземпляр пользователя для прямого доступа"""
    with app.app_context():
        return db.session.get(User, test_user)
