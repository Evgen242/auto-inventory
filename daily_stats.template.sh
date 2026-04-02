#!/bin/bash
# Ежедневная статистика
# Скопируйте в daily_stats.sh (токены будут взяты из .env)

DB_PATH="/var/www/apps/auto-inventory/instance/inventory.db"

# Загружаем переменные из .env
if [ -f /var/www/apps/auto-inventory/.env ]; then
    export $(grep -v '^#' /var/www/apps/auto-inventory/.env | xargs)
fi

# ... остальной код (см. daily_stats.sh)
