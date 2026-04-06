#!/bin/bash

APP_DIR="/var/www/apps/auto-inventory"
BACKUP_DIR="/var/backups/auto-inventory"
DB_FILE="$APP_DIR/instance/inventory.db"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

if [ -f "$DB_FILE" ]; then
    cp $DB_FILE $BACKUP_DIR/inventory_$DATE.db
    gzip -f $BACKUP_DIR/inventory_$DATE.db
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup created: inventory_$DATE.db.gz" >> $BACKUP_DIR/backup.log

    # Удаляем старые бэкапы (старше 30 дней)
    find $BACKUP_DIR -name "inventory_*.db.gz" -mtime +30 -delete
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Old backups cleaned" >> $BACKUP_DIR/backup.log
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Database not found!" >> $BACKUP_DIR/backup.log
fi
