import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

env_path = Path(__file__).parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://deploy:deploy_password_2026@localhost/auto_inventory"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Remember me cookie settings
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True

    # Session settings (важно для постоянной сессии)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SESSION_REFRESH_EACH_REQUEST = True
    SESSION_COOKIE_SECURE = False  # Временно для теста, при HTTPS можно True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    APP_NAME = "Auto Inventory System"
    APP_VERSION = "1.0.0"


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
