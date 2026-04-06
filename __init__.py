from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)

    # Настройка login manager
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Пожалуйста, авторизуйтесь для доступа к этой странице"
    login_manager.login_message_category = "info"

    # Регистрация blueprint
    from app.routes import auth, cars, main

    app.register_blueprint(auth.bp)
    app.register_blueprint(cars.bp)
    app.register_blueprint(main.bp)

    # Создание таблиц
    with app.app_context():
        db.create_all()

    return app
