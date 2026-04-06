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
    from app.routes import auth, cars, main, statistics

    app.register_blueprint(auth.bp)
    app.register_blueprint(cars.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(statistics.bp)

    # Создание таблиц
    with app.app_context():
        try:
            db.create_all()
            print("Database created successfully!")
        except Exception as e:
            print(f"Error creating database: {e}")

    return app


# Загрузка пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User

    # Используем db.session.get вместо устаревшего User.query.get
    return db.session.get(User, int(user_id))
