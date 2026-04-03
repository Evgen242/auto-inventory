#!/bin/bash

# Читаем Telegram настройки из .env
TELEGRAM_BOT_TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" /var/www/apps/auto-inventory/.env 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
TELEGRAM_CHAT_ID=$(grep "^TELEGRAM_CHAT_ID=" /var/www/apps/auto-inventory/.env 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)

# Получаем данные из базы данных
DB_PATH="/var/www/apps/auto-inventory/instance/inventory.db"
TOTAL_CARS=$(sqlite3 $DB_PATH "SELECT COUNT(*) FROM cars;" 2>/dev/null || echo "0")
TOTAL_BRANDS=$(sqlite3 $DB_PATH "SELECT COUNT(*) FROM car_brands;" 2>/dev/null || echo "0")
TOTAL_WAREHOUSES=$(sqlite3 $DB_PATH "SELECT COUNT(*) FROM warehouses;" 2>/dev/null || echo "0")
TOTAL_QUANTITY=$(sqlite3 $DB_PATH "SELECT SUM(quantity) FROM cars;" 2>/dev/null || echo "0")

# Формируем сообщение
MESSAGE="📊 Daily Report - Auto Inventory%0A%0A"
MESSAGE="${MESSAGE}🚗 Total cars: $TOTAL_CARS%0A"
MESSAGE="${MESSAGE}🏷️ Total brands: $TOTAL_BRANDS%0A"
MESSAGE="${MESSAGE}🏭 Total warehouses: $TOTAL_WAREHOUSES%0A"
MESSAGE="${MESSAGE}📦 Total units: $TOTAL_QUANTITY%0A"
MESSAGE="${MESSAGE}✅ Service status: Running%0A"
MESSAGE="${MESSAGE}📅 Date: $(date '+%Y-%m-%d %H:%M:%S')"

# Отправляем
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        -d "chat_id=$TELEGRAM_CHAT_ID" \
        -d "text=$MESSAGE" \
        -d "parse_mode=HTML" > /dev/null
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Daily stats sent" >> /var/log/auto-inventory-monitor.log
fi
