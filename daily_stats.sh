#!/bin/bash

# Читаем Telegram настройки из .env
if [ -f /var/www/apps/auto-inventory/config/.env ]; then
    TELEGRAM_BOT_TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" /var/www/apps/auto-inventory/config/.env | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
    TELEGRAM_CHAT_ID=$(grep "^TELEGRAM_CHAT_ID=" /var/www/apps/auto-inventory/config/.env | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
fi

# Параметры PostgreSQL
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="auto_inventory"
DB_USER="deploy"
DB_PASSWORD="deploy_password_2026"

export PGPASSWORD="$DB_PASSWORD"

# Получаем данные из PostgreSQL
TOTAL_CARS=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM cars;" 2>/dev/null | xargs || echo "0")
TOTAL_BRANDS=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM car_brands;" 2>/dev/null | xargs || echo "0")
TOTAL_WAREHOUSES=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM warehouses;" 2>/dev/null | xargs || echo "0")
TOTAL_QUANTITY=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COALESCE(SUM(quantity), 0) FROM cars;" 2>/dev/null | xargs || echo "0")
TOTAL_VALUE=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COALESCE(SUM(price * quantity), 0) FROM cars;" 2>/dev/null | xargs || echo "0")

# Формируем красивое сообщение
MESSAGE="📊 <b>ЕЖЕДНЕВНЫЙ ОТЧЕТ</b>%0A%0A"
MESSAGE="${MESSAGE}┌─────────────────────────────────┐%0A"
MESSAGE="${MESSAGE}│ 🚗 <b>Автомобилей:</b> $TOTAL_CARS%0A"
MESSAGE="${MESSAGE}│ 🏷️ <b>Марок:</b> $TOTAL_BRANDS%0A"
MESSAGE="${MESSAGE}│ 🏭 <b>Складов:</b> $TOTAL_WAREHOUSES%0A"
MESSAGE="${MESSAGE}│ 📦 <b>Единиц:</b> $TOTAL_QUANTITY%0A"
MESSAGE="${MESSAGE}│ 💰 <b>Стоимость:</b> ${TOTAL_VALUE} ₽%0A"
MESSAGE="${MESSAGE}│ ✅ <b>Статус:</b> Работает%0A"
MESSAGE="${MESSAGE}│ 📅 <b>Дата:</b> $(date '+%d.%m.%Y %H:%M:%S')%0A"
MESSAGE="${MESSAGE}└─────────────────────────────────┘"

# Отправляем
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d "chat_id=$TELEGRAM_CHAT_ID" \
        -d "text=$MESSAGE" \
        -d "parse_mode=HTML" > /dev/null
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Daily stats sent" >> /var/log/auto-inventory-monitor.log
fi
