#!/bin/bash
# Автоматическое восстановление сервисов

LOG_FILE="/var/log/auto-inventory-heal.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
}

# Проверка Production
if ! curl -s -f http://localhost:5000/health > /dev/null; then
    log "⚠️ Production не отвечает! Перезапуск..."
    sudo systemctl restart auto-inventory
    sleep 5
    if curl -s -f http://localhost:5000/health > /dev/null; then
        log "✅ Production восстановлен"
    else
        log "❌ Не удалось восстановить Production"
    fi
fi

# Проверка Docker
if ! curl -s -f http://localhost:5001/health > /dev/null; then
    log "⚠️ Docker не отвечает! Перезапуск..."
    cd /var/www/apps/auto-inventory
    docker compose -f docker-compose-dev.yml restart
    sleep 5
    if curl -s -f http://localhost:5001/health > /dev/null; then
        log "✅ Docker восстановлен"
    else
        log "❌ Не удалось восстановить Docker"
    fi
fi
