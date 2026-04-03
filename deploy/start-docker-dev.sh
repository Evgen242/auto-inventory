#!/bin/bash
# Запуск development версии в Docker

echo "🚀 Starting Docker development environment"

cd /var/www/apps/auto-inventory

# Экспортируем переменные
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Останавливаем старый контейнер если есть
docker-compose -f docker-compose-dev.yml down 2>/dev/null

# Собираем и запускаем
docker-compose -f docker-compose-dev.yml up -d --build

echo "⏳ Waiting for services to start..."
sleep 15

# Проверяем статус
echo ""
echo "📊 Container status:"
docker-compose -f docker-compose-dev.yml ps

# Проверяем здоровье приложения
echo ""
echo "🏥 Health check:"
curl -s http://localhost:5001/health | python3 -m json.tool || echo "Waiting for app to start..."

echo ""
echo "✅ Development environment running!"
echo "🌐 Access via Nginx: https://autolot25.ddns.net:8087"
echo "📊 Direct access: http://localhost:5001"
echo ""
echo "📋 Useful commands:"
echo "   docker-compose -f docker-compose-dev.yml logs -f    # View logs"
echo "   docker-compose -f docker-compose-dev.yml down       # Stop services"
