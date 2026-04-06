🚗 Auto Inventory System

text
     __________________
    /                 \
   |   🚘  🚙  🚗  🚕   |
   |   Автомобили на   |
   |     складах       |
   |__________________|
         ||    ||
         ||    ||
         oo    oo
https://github.com/Evgen242/auto-inventory/actions/workflows/check.yml/badge.svg
https://github.com/Evgen242/auto-inventory/actions/workflows/test.yml/badge.svg
https://img.shields.io/github/stars/Evgen242/auto-inventory
https://img.shields.io/github/forks/Evgen242/auto-inventory
https://img.shields.io/github/issues/Evgen242/auto-inventory

Система учета автомобилей на складах с авторизацией, поиском, фильтрацией и аналитикой.

🌐 Демо-доступ
Роль	Логин	Пароль	Права
👁️ Демо-пользователь	demo	demo123	Только просмотр
🔗 Демо версия: https://autolot25.ddns.net:8086

👑 Важно о правах администратора
Первый зарегистрированный пользователь автоматически получает права администратора!

💡 Совет: Зарегистрируйтесь первым, чтобы получить полный доступ к управлению системой.

✨ Возможности
🔐 Авторизация
Регистрация новых пользователей

Постоянные сессии (1 час бездействия)

"Запомнить меня" (7 дней)

Разграничение прав (демо / пользователь / администратор)

👥 Система ролей и прав
Действие	Демо	Обычный пользователь	Администратор
Просмотр автомобилей	✅	✅	✅
Поиск и фильтрация	✅	✅	✅
Просмотр статистики	✅	✅	✅
Добавление автомобилей	❌	✅	✅
Удаление СВОИХ автомобилей	❌	✅	✅
Удаление ЧУЖИХ автомобилей	❌	❌	✅
Редактирование автомобилей	❌	❌	✅
Управление марками	❌	❌	✅
Управление складами	❌	❌	✅
Админ-панель	❌	❌	✅
🏭 Управление складами
Создание складов с указанием местоположения

Отслеживание загрузки складов в реальном времени

🏷️ Управление марками
Добавление марок автомобилей

Удаление марок (только админ)

🚙 Учет автомобилей
Добавление автомобилей (модель, год, VIN, цена, количество)

Привязка к марке и складу

Автоматическая привязка к создателю

🔍 Поиск и фильтрация
Поиск по модели, VIN, марке

Фильтр по марке и складу

Фильтр по году выпуска (от/до)

Фильтр по цене (от/до)

Сортировка по любому полю

Пагинация

📊 Статистика и аналитика
Дашборд с ключевыми метриками

Распределение автомобилей по маркам

Загрузка складов

Топ самых дорогих автомобилей

Распределение по годам выпуска

🛠 Технологии
Компонент	Технология
Backend	Python 3.10, Flask, SQLAlchemy
Frontend	HTML5, CSS3, Bootstrap 5, JavaScript
Database	PostgreSQL
Server	Gunicorn, Nginx
Security	Flask-Login, Werkzeug, SSL
DevOps	Docker, GitHub Actions CI/CD
🚀 Быстрый старт
⚡ Автоматическое развертывание (рекомендуется)
Одна команда на любом Ubuntu сервере:

bash
curl -fsSL https://raw.githubusercontent.com/Evgen242/auto-inventory/main/deploy/auto-deploy.sh | bash
Скрипт автоматически установит Docker, настроит окружение и запустит приложение.

🐳 Ручное развертывание (Docker)
bash
git clone https://github.com/Evgen242/auto-inventory.git
cd auto-inventory
cp .env.docker.example .env.docker
docker compose -f docker-compose-dev.yml up -d
💻 Локальная установка
bash
git clone https://github.com/Evgen242/auto-inventory.git
cd auto-inventory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
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
🔧 CI/CD (GitHub Actions)
Workflow	Триггер	Действие
check.yml	Push в main	Проверка качества кода
test.yml	Push в main	Линтинг и проверка секретов
📁 Структура проекта
text
auto-inventory/
├── app/                    # Основное приложение
│   ├── models/            # Модели данных
│   ├── routes/            # Маршруты API
│   └── templates/         # HTML шаблоны
├── tests/                 # Тесты
├── deploy/                # Скрипты деплоя
├── Dockerfile             # Docker образ
├── docker-compose-dev.yml # Docker Compose
├── requirements.txt       # Python зависимости
└── README.md             # Документация
🛠 Команды для разработки
bash
make test-all      # Запуск всех тестов
make coverage      # Тесты с покрытием
make clean         # Очистка кэша
make pre-commit    # Проверка форматирования
🐛 Устранение неполадок
Проблема	Решение
Не удается войти	Зарегистрируйтесь через форму регистрации
Сессия сбрасывается	Проверьте SECRET_KEY в .env
Docker не запускается	docker compose down -v && docker compose up -d --build
Нет места на диске	docker system prune -a -f --volumes
📝 Лицензия
MIT License

👨‍💻 Автор
Evgenii Fralou (Evgen242)

https://img.shields.io/badge/GitHub-@Evgen242-181717?style=flat&logo=github

⭐️ Если проект вам полезен, поставьте звезду на GitHub!
text
    ⭐️
   /   \
  |  ❤️  |
   \___/
Спасибо за внимание! 🚀
