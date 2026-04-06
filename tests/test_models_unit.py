"""Unit-тесты для моделей данных"""
import pytest
from app import db
from app.models.user import User


class TestUserModel:
    """Тесты модели User"""

    def test_create_user(self, app):
        """Тест создания пользователя"""
        with app.app_context():
            user = User(username="testuser", email="test@example.com")
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.username == "testuser"
            assert user.email == "test@example.com"
            assert user.check_password("password123") is True
            assert user.check_password("wrong") is False
            assert user.is_admin is False

    def test_admin_user(self, app):
        """Тест прав администратора"""
        with app.app_context():
            admin = User(username="admin", email="admin@example.com", is_admin=True)
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

            assert admin.is_admin is True

    def test_user_to_dict(self, app):
        """Тест сериализации пользователя"""
        with app.app_context():
            user = User(username="serialize", email="serialize@example.com")
            user.set_password("pass")
            db.session.add(user)
            db.session.commit()

            user_dict = user.to_dict()

            assert "id" in user_dict
            assert "username" in user_dict
            assert "email" in user_dict
            assert user_dict["username"] == "serialize"
            assert "password_hash" not in user_dict

    def test_unique_username_constraint(self, app):
        """Тест уникальности username"""
        with app.app_context():
            user1 = User(username="unique", email="unique1@example.com")
            user1.set_password("pass")
            db.session.add(user1)
            db.session.commit()

            user2 = User(username="unique", email="unique2@example.com")
            user2.set_password("pass")
            db.session.add(user2)

            with pytest.raises(Exception):
                db.session.commit()
            db.session.rollback()

    def test_user_repr(self, app):
        """Тест строкового представления"""
        with app.app_context():
            user = User(username="reprtest", email="repr@example.com")
            assert "reprtest" in repr(user)

    def test_password_hashing(self, app):
        """Тест хэширования пароля"""
        with app.app_context():
            user = User(username="hashuser", email="hash@example.com")
            password = "SecurePass123!"
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            assert user.password_hash != password
            assert user.check_password(password) is True
            assert user.check_password("wrong") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
