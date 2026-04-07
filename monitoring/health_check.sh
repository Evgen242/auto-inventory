#!/bin/bash
# Комплексная проверка здоровья приложения

echo "=== AUTO-INVENTORY HEALTH CHECK ==="
echo "Время: $(date)"
echo ""

# 1. Проверка Production
echo "📡 Production (8086):"
if curl -s -f http://localhost:5000/health > /dev/null; then
    echo "  ✅ API работает"
else
    echo "  ❌ API НЕ РАБОТАЕТ"
fi

# 2. Проверка Docker (8087)
echo "🐳 Docker (8087):"
if curl -s -f http://localhost:5001/health > /dev/null; then
    echo "  ✅ API работает"
else
    echo "  ❌ API НЕ РАБОТАЕТ"
fi

# 3. Проверка базы данных
echo "🗄️ PostgreSQL:"
if docker exec auto_inventory_postgres_dev pg_isready -U deploy > /dev/null 2>&1; then
    echo "  ✅ Docker БД работает"
else
    echo "  ❌ Docker БД НЕ РАБОТАЕТ"
fi

if sudo -u postgres psql -c "SELECT 1" > /dev/null 2>&1; then
    echo "  ✅ Production БД работает"
else
    echo "  ❌ Production БД НЕ РАБОТАЕТ"
fi

# 4. Проверка диска
echo "💾 Диск:"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -lt 80 ]; then
    echo "  ✅ Свободно: $(df -h / | awk 'NR==2 {print $4}')"
else
    echo "  ⚠️ ВНИМАНИЕ! Мало места: $DISK_USAGE% использовано"
fi

# 5. Проверка памяти
echo "🧠 Память:"
FREE_MEM=$(free -m | awk 'NR==2 {print $7}')
if [ $FREE_MEM -gt 200 ]; then
    echo "  ✅ Свободно: ${FREE_MEM}MB"
else
    echo "  ⚠️ ВНИМАНИЕ! Мало памяти: ${FREE_MEM}MB свободно"
fi

# 6. Проверка бэкапов
echo "💾 Бэкапы:"
LAST_BACKUP=$(ls -t /var/backups/auto-inventory/*.sql.gz 2>/dev/null | head -1)
if [ -n "$LAST_BACKUP" ]; then
    BACKUP_DATE=$(stat -c %y "$LAST_BACKUP" | cut -d' ' -f1)
    echo "  ✅ Последний бэкап: $BACKUP_DATE"
else
    echo "  ❌ Нет бэкапов!"
fi

echo ""
echo "=== HEALTH CHECK COMPLETED ==="
