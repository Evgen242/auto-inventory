# 🚘  🚙   Auto Inventory System  🚗  🚕

[![Code Quality](https://github.com/Evgen242/auto-inventory/actions/workflows/check.yml/badge.svg)](https://github.com/Evgen242/auto-inventory/actions/workflows/check.yml)
[![Tests](https://github.com/Evgen242/auto-inventory/actions/workflows/test.yml/badge.svg)](https://github.com/Evgen242/auto-inventory/actions/workflows/test.yml)
[![GitHub stars](https://img.shields.io/github/stars/Evgen242/auto-inventory)](https://github.com/Evgen242/auto-inventory/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Evgen242/auto-inventory)](https://github.com/Evgen242/auto-inventory/network)
[![GitHub issues](https://img.shields.io/github/issues/Evgen242/auto-inventory)](https://github.com/Evgen242/auto-inventory/issues)

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

> 💡 **Совет:** Если вы первый пользователь системы, зарегистрируйтесь сразу после установки, чтобы получить полный доступ.

---

## ✨ Возможности

### 🔐 Авторизация
- Регистрация новых пользователей
- Постоянные сессии (1 час бездействия)
- "Запомнить меня" (7 дней)
- Разграничение прав (демо / пользователь / администратор)

### 👥 Система ролей и прав

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

### 🏭 Управление складами
- Создание складов с указанием местоположения
- Отслеживание загрузки складов в реальном времени

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
- Загрузка складов
- Топ самых дорогих автомобилей
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
| **DevOps** | Docker, GitHub Actions CI/CD |

---

## 🚀 Быстрый старт

### Автоматическое развертывание (рекомендуется)

**Одна команда на любом Ubuntu сервере:**

```bash
curl -fsSL https://raw.githubusercontent.com/Evgen242/auto-inventory/main/deploy/auto-deploy.sh | bash
Скрипт автоматически:

Установит Docker и Docker Compose

Клонирует репозиторий

Настроит окружение

Запустит приложение

Ручное развертывание
Вариант 1: Docker (рекомендуется)
bash
# Клонирование репозитория
git clone https://github.com/Evgen242/auto-inventory.git
cd auto-inventory

# Копирование конфигурации (шаблон → реальный файл)
cp config/.env.example config/.env.docker

# Запуск
docker compose -f docker-compose-dev.yml up -d

# Проверка статуса
docker compose -f docker-compose-dev.yml ps

# Просмотр логов
docker compose -f docker-compose-dev.yml logs -f

# Остановка
docker compose -f docker-compose-dev.yml down
Вариант 2: Локальная установка
bash
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
cp config/.env.example .env
# Отредактируйте .env (SECRET_KEY, DATABASE_URL)

# Запуск приложения
python run.py
🐳 Docker команды
bash
# Запуск с пересборкой
docker compose -f docker-compose-dev.yml up -d --build

# Просмотр статуса
docker compose -f docker-compose-dev.yml ps

# Логи приложения
docker compose -f docker-compose-dev.yml logs -f app-dev

# Вход в контейнер
docker exec -it auto_inventory_app_dev bash

# Остановка с удалением томов
docker compose -f docker-compose-dev.yml down -v
👥 Управление пользователями
Регистрация первого пользователя (становится администратором)
Просто откройте приложение в браузере и нажмите "Зарегистрироваться". Первый зарегистрированный пользователь автоматически получит права администратора.

Создание пользователя через командную строку (опционально)
bash
docker exec auto_inventory_app_dev python3 -c "
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    user = User(username='username', email='user@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    print('✅ User created')
"
Назначение администратором существующего пользователя
bash
docker exec auto_inventory_app_dev python3 -c "
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='username').first()
    user.is_admin = True
    db.session.commit()
    print(f'✅ {user.username} теперь администратор')
"
🤖 Telegram уведомления
Система отправляет уведомления о:

Входе администратора

Регистрации нового пользователя

Ежедневной статистике (через cron)

Проблемах с сервером (автоматическое восстановление)

Настройка
Создайте бота в Telegram через @BotFather.

Получите токен (например, 123456:ABC...).

Узнайте свой chat_id (напишите боту любое сообщение, затем выполните:

bash
curl -s "https://api.telegram.org/bot<ТОКЕН>/getUpdates" | grep chat
Добавьте в config/.env (или config/.env.docker для Docker) строки:

ini
TELEGRAM_BOT_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_id
Перезапустите приложение.

💡 Тестовое сообщение: ./daily_stats.sh отправит текущую статистику.

📊 Мониторинг и бэкапы
Проверка здоровья сервисов
bash
./monitoring/health_check.sh
Автоматическое восстановление (auto-heal)
Скрипт monitoring/auto_heal.sh перезапускает упавшие сервисы. Добавлен в cron:

bash
*/5 * * * * /var/www/apps/auto-inventory/monitoring/auto_heal.sh
Бэкапы
Ежедневно в 2:00 создаётся бэкап PostgreSQL (production и Docker), конфигов и Docker volume.

Старые бэкапы (старше 30 дней) удаляются автоматически.

Логи бэкапов: /var/backups/auto-inventory/backup.log

Запуск вручную: ./backup.sh

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
GET	/api/me	Информация о текущем пользователе	✅ Авторизованные
Пример использования API
bash
# Логин
curl -c cookies.txt -X POST http://localhost:5000/auth/login \
  -d "username=username" -d "password=password123"

# Получение списка автомобилей
curl -b cookies.txt http://localhost:5000/api/cars

# Получение статистики
curl -b cookies.txt http://localhost:5000/api/stats

# Получение информации о пользователе
curl -b cookies.txt http://localhost:5000/api/me
🔧 CI/CD (GitHub Actions)
Workflow	Триггер	Действие
check.yml	Push в main	Проверка качества кода (flake8, black)
test.yml	Push в main	Линтинг и проверка секретов
dockerhub.yml	Push в main	Сборка и публикация образа в Docker Hub
📁 Структура проекта
text
auto-inventory/
├── app/                    # Основное приложение
│   ├── models/            # Модели данных
│   ├── routes/            # Маршруты API
│   └── templates/         # HTML шаблоны
├── config/                # Конфигурация (.env, .env.docker, .env.example)
├── deploy/                # Скрипты деплоя
├── monitoring/            # Скрипты мониторинга и авто-восстановления
├── tests/                 # Тесты
├── Dockerfile             # Docker образ
├── docker-compose-dev.yml # Docker Compose (development)
├── docker-compose.prod.yml# Docker Compose (production)
├── requirements.txt       # Python зависимости
├── config.py              # Конфигурация приложения
├── Makefile               # Команды для разработки
└── README.md              # Документация
🛠 Команды для разработки
bash
# Запуск всех тестов
make test-all

# Только unit тесты
make test-unit

# Тесты с покрытием
make coverage

# Очистка кэша
make clean

# Проверка форматирования
make pre-commit
🐛 Устранение неполадок
Проблема	Решение
"Please check your username and password"	Зарегистрируйтесь через форму регистрации или создайте пользователя через командную строку
Сессия сбрасывается при обновлении	Проверьте, что SECRET_KEY одинаковый для всех экземпляров
Docker не запускается	Очистите и пересоберите: docker compose -f docker-compose-dev.yml down -v && docker compose -f docker-compose-dev.yml up -d --build
Нет места на диске	Очистите Docker: docker system prune -a -f --volumes и логи: sudo journalctl --vacuum-size=50M
📝 Лицензия
MIT License

👨‍💻 Автор
Evgenii Fralou (Evgen242)

GitHub: @Evgen242

⭐️ Если проект вам полезен, поставьте звезду на GitHub!
