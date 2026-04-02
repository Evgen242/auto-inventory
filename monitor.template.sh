#!/bin/bash
# Мониторинг приложения
# Скопируйте в monitor.sh (токены будут взяты из .env)

APP_URL="http://localhost:5000/health"
LOG_FILE="/var/log/auto-inventory-monitor.log"

# Загружаем переменные из .env
if [ -f /var/www/apps/auto-inventory/.env ]; then
    export $(grep -v '^#' /var/www/apps/auto-inventory/.env | xargs)
fi

# ... остальной код (см. monitor.sh)
