# 🚗 Auto Inventory System

[![Deploy to Production](https://github.com/Evgen242/auto-inventory/actions/workflows/deploy.yml/badge.svg)](https://github.com/Evgen242/auto-inventory/actions/workflows/deploy.yml)
[![Code Quality](https://github.com/Evgen242/auto-inventory/actions/workflows/check.yml/badge.svg)](https://github.com/Evgen242/auto-inventory/actions/workflows/check.yml)

**Система учета автомобилей на складах** с авторизацией, поиском, фильтрацией и аналитикой.

---

## 🌐 Демо-доступ

| Роль | Логин | Пароль | Права |
|------|-------|--------|-------|
| 👁️ **Демо-пользователь** | `demo` | `demo123` | Только просмотр |

🔗 **Демо версия:** https://autolot25.ddns.net:8086

---

## 👑 Важно о правах администратора

**Первый зарегистрированный пользователь автоматически получает права администратора!**

Это сделано для удобства первоначальной настройки системы. Все последующие пользователи регистрируются с обычными правами.

### Как стать администратором:
1. Зарегистрируйтесь первым в системе
2. Вы автоматически получите все права администратора
3. Сможете управлять марками, складами и другими пользователями

### Проверка прав:
- Администратор видит пункт "Админ-панель" в меню
- Администратор может удалять любые автомобили
- Администратор управляет справочниками (марки, склады)

> 💡 **Совет:** Если вы первый пользователь системы, зарегистрируйтесь сразу после установки, чтобы получить полный доступ.

---

## 👤 Система ролей и прав

| Действие | Демо | Обычный пользователь | Администратор |
|----------|:----:|:-------------------:|:-------------:|
| **Просмотр автомобилей** | ✅ | ✅ | ✅ |
| **Поиск и фильтрация** | ✅ | ✅ | ✅ |
| **Просмотр статистики** | ✅ | ✅ | ✅ |
| **Добавление автомобилей** | ❌ | ✅ | ✅ |
| **Удаление СВОИХ автомобилей** | ❌ | ✅ | ✅ |
| **Удаление ЧУЖИХ автомобилей** | ❌ | ❌ | ✅ |
| **Редактирование автомобилей** | ❌ | ❌ | ✅ |
| **Управление марками** | ❌ | ❌ | ✅ |
| **Управление складами** | ❌ | ❌ | ✅ |
| **Админ-панель** | ❌ | ❌ | ✅ |

---

## ✨ Возможности

### 🔐 Авторизация
- Регистрация новых пользователей
- Вход с сохранением сессии
- Разграничение прав (демо / пользователь / администратор)

### 🏭 Управление складами
- Создание складов с указанием местоположения
- Отслеживание загрузки складов (в %)

### 🏷️ Управление марками
- Добавление марок автомобилей
- Удаление марок (только админ)

### 🚙 Учет автомобилей
- Добавление автомобилей (модель, год, VIN, цена, количество)
- Привязка к марке и складу
- Автоматическая привязка к создателю

### 🔍 Поиск и фильтрация
- Поиск по модели, VIN, марке
- Фильтр по марке и складу
- Фильтр по году выпуска (от/до)
- Фильтр по цене (от/до)
- Сортировка по любому полю
- Пагинация

### 📊 Статистика и аналитика
- Дашборд с ключевыми метриками
- Распределение автомобилей по маркам
- Загрузка складов в реальном времени
- Топ 5 самых дорогих автомобилей
- Распределение по годам выпуска

---

## 🛠 Технологии

| Компонент | Технология |
|-----------|------------|
| **Backend** | Python 3.10, Flask, SQLAlchemy |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Database** | PostgreSQL |
| **Server** | Gunicorn, Nginx |
| **Security** | Flask-Login, Werkzeug, SSL |
| **DevOps** | GitHub Actions CI/CD |

---

## 🚀 Быстрый старт

### Локальная установка

```bash
# Клонирование репозитория
git clone https://github.com/Evgen242/auto-inventory.git
cd auto-inventory

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env (SECRET_KEY, DATABASE_URL)

# Запуск приложения
python run.py
Docker поддержка
bash
# Запуск в Docker
docker compose -f docker-compose-dev.yml up -d

# Просмотр статуса
docker compose -f docker-compose-dev.yml ps

# Просмотр логов
docker compose -f docker-compose-dev.yml logs -f

# Остановка
docker compose -f docker-compose-dev.yml down
👥 Управление пользователями в Docker
bash
# Добавление нового пользователя
docker exec auto_inventory_app_dev python3 -c "
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    user = User(username='newuser', email='new@example.com', is_admin=False)
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    print('✅ User created')
"

# Просмотр всех пользователей
docker exec auto_inventory_app_dev python3 -c "
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    for user in User.query.all():
        admin_status = '👑' if user.is_admin else '👤'
        print(f'{admin_status} {user.username} (admin: {user.is_admin})'
"

# Назначение администратора
docker exec auto_inventory_app_dev python3 -c "
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='username').first()
    if user:
        user.is_admin = True
        db.session.commit()
        print(f'✅ {user.username} теперь администратор')
"
📡 API Endpoints
Метод	Endpoint	Описание	Доступ
GET	/api/cars	Список автомобилей	✅ Авторизованные
POST	/api/cars	Добавить авто	✅ Кроме demo
DELETE	/api/cars/<id>	Удалить авто	✅ Свои - пользователь, любые - админ
GET	/api/brands	Список марок	✅ Авторизованные
POST	/api/brands	Добавить марку	✅ Только админ
GET	/api/warehouses	Список складов	✅ Авторизованные
POST	/api/warehouses	Добавить склад	✅ Только админ
GET	/api/stats	Статистика	✅ Авторизованные
🔧 CI/CD (GitHub Actions)
Workflow	Триггер	Действие
deploy.yml	Push в main	Автоматический деплой на сервер
check.yml	Push в main	Проверка качества кода (flake8)
backup.yml	Каждый день в 2:00	Резервное копирование БД
📝 Лицензия
MIT License

👨‍💻 Автор
Evgenii Fralou (Evgen242)

GitHub: @Evgen242

⭐️ Если проект вам полезен, поставьте звезду на GitHub!
# CI/CD Test Fri Apr  3 12:23:15 PM UTC 2026
