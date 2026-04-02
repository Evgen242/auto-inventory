# 🚗 Auto Inventory System

Система учета автомобилей на складах с авторизацией, поиском и аналитикой.

## ✨ Возможности

- 🔐 **Авторизация** - регистрация и вход пользователей
- 🏭 **Управление складами** - создание и отслеживание складов
- 🏷️ **Управление марками** - добавление и удаление марок авто
- 🚙 **Учет автомобилей** - добавление авто с указанием марки, склада, цены
- 🔍 **Поиск и фильтрация** - поиск по модели, VIN, марке
- 📊 **Статистика** - дашборд с графиками и аналитикой
- 📱 **Адаптивный дизайн** - Bootstrap 5

## 🛠 Технологии

| Компонент | Технология |
|-----------|------------|
| Backend | Python 3.10, Flask, SQLAlchemy |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Database | SQLite |
| Server | Gunicorn, Nginx |
| Security | Flask-Login, Werkzeug, SSL |

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

# Запуск приложения
python3 run.py
Production настройка
# Запуск через Gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 run:app

# systemd сервис
sudo systemctl start auto-inventory
sudo systemctl enable auto-inventory
📊 API Endpoints
Метод	Endpoint	Описание	Доступ
GET	/api/cars	Список автомобилей	Авторизованные
POST	/api/cars	Добавить авто	Авторизованные
GET	/api/brands	Список марок	Авторизованные
POST	/api/brands	Добавить марку	Только админ
GET	/api/warehouses	Список складов	Авторизованные
POST	/api/warehouses	Добавить склад	Только админ
GET	/api/stats	Статистика	Авторизованные
👨‍💻 Автор
Evgenii Fralou (Evgen242)

📝 Лицензия
MIT License - свободное использование, модификация и распространение

⭐️ Поставьте звезду, если проект вам полезен!

## 🚀 CI/CD Status

[![Deploy to Production](https://github.com/Evgen242/auto-inventory/actions/workflows/deploy.yml/badge.svg)](https://github.com/Evgen242/auto-inventory/actions/workflows/deploy.yml)
[![Code Quality](https://github.com/Evgen242/auto-inventory/actions/workflows/check.yml/badge.svg)](https://github.com/Evgen242/auto-inventory/actions/workflows/check.yml)
[![Backup](https://github.com/Evgen242/auto-inventory/actions/workflows/backup.yml/badge.svg)](https://github.com/Evgen242/auto-inventory/actions/workflows/backup.yml)

Автоматический деплой при пуше в main ветку.
