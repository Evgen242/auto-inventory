#!/bin/bash

APP_DIR="/var/www/apps/auto-inventory"
BACKUP_DIR="/var/backups/auto-inventory"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

echo "=========================================" >> $BACKUP_DIR/backup.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting backup..." >> $BACKUP_DIR/backup.log

# 1. Бэкап PostgreSQL (production)
if docker ps | grep -q auto_inventory_postgres_dev; then
    # Docker PostgreSQL
    docker exec auto_inventory_postgres_dev pg_dump -U deploy auto_inventory_dev | gzip > $BACKUP_DIR/docker_db_$DATE.sql.gz
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Docker PostgreSQL backup created" >> $BACKUP_DIR/backup.log
fi

# 2. Бэкап локального PostgreSQL (если есть)
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw auto_inventory; then
    sudo -u postgres pg_dump auto_inventory | gzip > $BACKUP_DIR/prod_db_$DATE.sql.gz
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Production PostgreSQL backup created" >> $BACKUP_DIR/backup.log
fi

# 3. Бэкап .env и конфигурации
cp $APP_DIR/config/.env $BACKUP_DIR/env_$DATE.backup 2>/dev/null
cp $APP_DIR/config.py $BACKUP_DIR/config_$DATE.backup 2>/dev/null
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Config files backed up" >> $BACKUP_DIR/backup.log

# 4. Бэкап Docker volume (опционально)
docker run --rm -v auto_inventory_postgres_dev_data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/docker_volume_$DATE.tar.gz -C /data . 2>/dev/null
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Docker volume backed up" >> $BACKUP_DIR/backup.log

# 5. Удаляем старые бэкапы (старше 30 дней)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.backup" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Old backups cleaned" >> $BACKUP_DIR/backup.log
echo "=========================================" >> $BACKUP_DIR/backup.log

# 6. Отчет о размере бэкапов
BACKUP_SIZE=$(du -sh $BACKUP_DIR | cut -f1)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Total backup size: $BACKUP_SIZE" >> $BACKUP_DIR/backup.log

echo "✅ Backup completed: $DATE"
