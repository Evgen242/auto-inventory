#!/bin/bash

# Настройки
APP_URL="http://localhost:5000/health"
LOG_FILE="/var/log/auto-inventory-monitor.log"

# Читаем Telegram настройки напрямую из .env
TELEGRAM_BOT_TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" /var/www/apps/auto-inventory/config/.env 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
TELEGRAM_CHAT_ID=$(grep "^TELEGRAM_CHAT_ID=" /var/www/apps/auto-inventory/config/.env 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)

# Функция отправки в Telegram
send_telegram() {
    local message="$1"
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ "$TELEGRAM_BOT_TOKEN" != "your_bot_token_here" ]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID" \
            -d "text=$message" \
            -d "parse_mode=HTML" > /dev/null 2>&1
    fi
}

# Проверка приложения
check_app() {
    local response=$(curl -s -o /dev/null -w "%{http_code}" $APP_URL 2>/dev/null)

    if [ "$response" == "200" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Application is healthy" >> $LOG_FILE
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Application is DOWN! HTTP $response" >> $LOG_FILE
        send_telegram "🚨 Auto Inventory Alert! Application is DOWN! HTTP $response"
    fi
}

# Запуск
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting monitoring check..." >> $LOG_FILE
check_app
echo "---" >> $LOG_FILE
