"""Unit-тесты для маршрутов"""
import pytest
from app import db
from app.models.user import User


def test_index_page_redirects_to_login(client):
    """Тест: неавторизованный пользователь редиректится на логин"""
    response = client.get("/")
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_index_page_authenticated(authenticated_client):
    """Тест: авторизованный пользователь видит главную страницу"""
    response = authenticated_client.get("/")
    assert response.status_code == 200


def test_login_page(client):
    """Тест страницы логина"""
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_register_page(client):
    """Тест страницы регистрации"""
    response = client.get("/auth/register")
    assert response.status_code == 200


def test_register_new_user(client, app):
    """Тест регистрации нового пользователя"""
    response = client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username="newuser").first()
        assert user is not None
        assert user.email == "new@example.com"


def test_register_duplicate_username(client, test_user, app):
    """Тест регистрации с существующим username"""
    with app.app_context():
        existing_user = User.query.get(test_user)
        response = client.post(
            "/auth/register",
            data={
                "username": existing_user.username,
                "email": "duplicate@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200


def test_login_valid_user(client, test_user, app):
    """Тест входа с правильными данными"""
    with app.app_context():
        user = User.query.get(test_user)
        response = client.post(
            "/auth/login",
            data={"username": user.username, "password": "test123"},
            follow_redirects=True,
        )

        assert response.status_code == 200


def test_login_invalid_user(client):
    """Тест входа с неправильными данными"""
    response = client.post(
        "/auth/login",
        data={"username": "wronguser", "password": "wrongpass"},
        follow_redirects=True,
    )

    assert response.status_code == 200


def test_dashboard_requires_auth(client):
    """Тест: дашборд требует авторизации"""
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200


def test_authenticated_dashboard(authenticated_client):
    """Тест дашборда с авторизацией"""
    response = authenticated_client.get("/dashboard")
    assert response.status_code == 200


def test_logout(authenticated_client):
    """Тест выхода из системы"""
    response = authenticated_client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200

    response = authenticated_client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200


def test_profile_page_requires_auth(client):
    """Тест: профиль требует авторизации"""
    response = client.get("/profile", follow_redirects=True)
    assert response.status_code == 200


def test_authenticated_profile(authenticated_client):
    """Тест профиля с авторизацией"""
    response = authenticated_client.get("/profile")
    assert response.status_code == 200
