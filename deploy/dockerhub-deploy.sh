#!/bin/bash
# Деплой из Docker Hub

set -e

echo "🚀 Deploying from Docker Hub..."

# Загрузка переменных
if [ -f config/config/.env.prod ]; then
    export $(grep -v '^#' config/config/.env.prod | xargs)
fi

# Pull последних образов
docker pull evgen242/auto-inventory:latest
docker pull postgres:13

# Запуск
docker compose -f docker-compose.prod.yml up -d

# Проверка
sleep 10
curl -s http://localhost:5000/health

echo "✅ Deployed from Docker Hub!"
