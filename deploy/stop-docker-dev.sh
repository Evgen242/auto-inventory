#!/bin/bash
# Остановка development версии в Docker

echo "🛑 Stopping Docker development environment"

cd /var/www/apps/auto-inventory
docker-compose -f docker-compose-dev.yml down

echo "✅ Development environment stopped"
