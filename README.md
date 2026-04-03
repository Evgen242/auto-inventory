# 🚗 Auto Inventory System

[![Deploy to Production](https://github.com/Evgen242/auto-inventory/actions/workflows/deploy.yml/badge.svg)](https://github.com/Evgen242/auto-inventory/actions/workflows/deploy.yml)
[![Code Quality](https://github.com/Evgen242/auto-inventory/actions/workflows/check.yml/badge.svg)](https://github.com/Evgen242/auto-inventory/actions/workflows/check.yml)

**Система учета автомобилей на складах** с авторизацией, поиском, фильтрацией и аналитикой.

---

## 🌐 Демо-доступ

| Роль | Логин | Пароль | Права |
|------|-------|--------|-------|
| 👁️ **Демо-пользователь** | `demo` | `demo123` | Только просмотр |

🔗 **Production:** https://autolot25.ddns.net:8086

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
- Удаление складов (только админ)

### 🏷️ Управление марками
- Добавление марок автомобилей
- Удаление марок (только админ)

### 🚙 Учет автомобилей
- Добавление автомобилей (модель, год, VIN, цена, количество)
- Привязка к марке и складу
- Автоматическая привязка к создателю
- Удаление (свои - пользователь, любые - админ)

### 🔍 Поиск и фильтрация
- Поиск по модели, VIN, марке
- Фильтр по марке и складу
- Фильтр по году выпуска (от/до)
- Фильтр по цене (от/до)
- Сортировка по любому полю
- Пагинация (20 записей на странице)

### 📊 Статистика и аналитика
- Дашборд с ключевыми метриками
- Распределение автомобилей по маркам
- Загрузка складов в реальном времени
- Топ 5 самых дорогих автомобилей
- Топ 5 по количеству на складах
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

## 📊 Текущая статистика

- 🚗 **Автомобилей:** 15+ моделей
- 🏷️ **Марок:** 10+
- 🏭 **Складов:** 8
- 📦 **Всего единиц:** 1000+

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
python3 run.py
Production настройка
bash
# Запуск через Gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 run:app

# Настройка systemd сервиса
sudo systemctl start auto-inventory
sudo systemctl enable auto-inventory
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

---

## 🐳 Docker Контейнеризация

### Development окружение в Docker

Проект поддерживает запуск в Docker контейнерах для изолированной разработки и тестирования.

#### 📋 Состав Docker окружения

| Компонент | Контейнер | Порт | База данных |
|-----------|-----------|------|--------------|
| **Приложение** | auto_inventory_app_dev | 5001 (внутренний) | - |
| **PostgreSQL** | auto_inventory_postgres_dev | 5433 (внешний) | auto_inventory_dev |
| **Nginx Proxy** | - | 8087 (внешний) | - |

#### 🚀 Быстрый запуск Docker версии

```bash
# Переход в директорию проекта
cd /var/www/apps/auto-inventory

# Запуск контейнеров
docker compose -f docker-compose-dev.yml up -d

# Проверка статуса
docker compose -f docker-compose-dev.yml ps

# Просмотр логов
docker compose -f docker-compose-dev.yml logs -f
🛠️ Управление Docker контейнерами
bash
# Запуск через скрипт
./deploy/start-docker-dev.sh

# Остановка через скрипт
./deploy/stop-docker-dev.sh

# Перезапуск контейнеров
docker compose -f docker-compose-dev.yml restart

# Остановка с удалением volumes
docker compose -f docker-compose-dev.yml down -v

# Просмотр использования ресурсов
docker stats
🔗 Доступ к Docker версии
Окружение	URL	Порт	Статус
Development	https://autolot25.ddns.net:8087	8087	✅ Работает
Production	https://autolot25.ddns.net:8086	8086	✅ Работает
📝 Учетные записи для Docker
Роль	Логин	Пароль	Права
Администратор	user	При регистрации	Полный доступ
Демо-пользователь	demo	demo123	Только просмотр
🗄️ Управление пользователями в Docker
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
        print(f'{user.username} (admin: {user.is_admin})')
"
📊 Мониторинг Docker версии
bash
# Проверка здоровья приложения
curl http://localhost:5001/health

# Проверка через Nginx
curl -k https://autolot25.ddns.net:8087/health

# Просмотр логов в реальном времени
docker compose -f docker-compose-dev.yml logs -f --tail=50

# Проверка подключения к БД
docker exec auto_inventory_postgres_dev pg_isready -U deploy
🐛 Отладка Docker контейнера
bash
# Вход в контейнер приложения
docker exec -it auto_inventory_app_dev bash

# Вход в контейнер PostgreSQL
docker exec -it auto_inventory_postgres_dev bash

# Проверка переменных окружения
docker exec auto_inventory_app_dev env | grep DATABASE

# Просмотр логов конкретного контейнера
docker logs auto_inventory_app_dev --tail=100
docker logs auto_inventory_postgres_dev --tail=50
🔧 Структура Docker файлов
text
auto-inventory/
├── Dockerfile                    # Образ приложения
├── docker-compose-dev.yml        # Development окружение
├── .docker_version              # Версия Docker образа
└── deploy/
    ├── start-docker-dev.sh      # Скрипт запуска
    ├── stop-docker-dev.sh       # Скрипт остановки
    └── docker-status.sh         # Проверка статуса
⚙️ Переменные окружения для Docker
Переменная	Значение	Описание
DATABASE_URL	postgresql://deploy:deploy_password_2026@postgres-dev:5432/auto_inventory_dev	Подключение к PostgreSQL
SECRET_KEY	dev-secret-key-2026	Секретный ключ Flask
FLASK_ENV	development	Режим работы Flask
💾 Бэкап базы данных Docker
bash
# Экспорт базы данных
docker exec auto_inventory_postgres_dev pg_dump -U deploy auto_inventory_dev > backup_$(date +%Y%m%d).sql

# Восстановление базы данных
docker exec -i auto_inventory_postgres_dev psql -U deploy auto_inventory_dev < backup_20250403.sql
🎯 Преимущества Docker версии
✅ Изолированное окружение - не влияет на продакшен

✅ Быстрый запуск - одна команда для развертывания

✅ Легкое тестирование - безопасное тестирование новых функций

✅ Единая конфигурация - одинаковые настройки для всех разработчиков

✅ Простое обновление - пересборка образа одной командой

🔗 Ссылки
Production: https://autolot25.ddns.net:8086

Development (Docker): https://autolot25.ddns.net:8087

GitHub: https://github.com/Evgen242/auto-inventory

📞 Поддержка
При возникновении проблем:

Проверьте логи: docker compose -f docker-compose-dev.yml logs

Проверьте статус: docker compose -f docker-compose-dev.yml ps

Проверьте health: curl -k https://autolot25.ddns.net:8087/health

Перезапустите контейнеры: docker compose -f docker-compose-dev.yml restart

