#!/bin/bash
# Автоматическое развертывание Auto-Inventory на Ubuntu сервере

set -e

echo "🚀 Auto-Inventory Auto-Deploy Script"
echo "====================================="

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Проверка системы
echo -e "\n${YELLOW}1. Проверка системы...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker не установлен. Устанавливаем...${NC}"
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo -e "${GREEN}✅ Docker установлен${NC}"
else
    echo -e "${GREEN}✅ Docker уже установлен${NC}"
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Устанавливаем Docker Compose...${NC}"
    sudo apt install docker-compose -y
    echo -e "${GREEN}✅ Docker Compose установлен${NC}"
else
    echo -e "${GREEN}✅ Docker Compose уже установлен${NC}"
fi

# 2. Клонирование или обновление
echo -e "\n${YELLOW}2. Клонирование репозитория...${NC}"
if [ -d "auto-inventory" ]; then
    cd auto-inventory
    git pull origin main
    cd ..
else
    git clone https://github.com/Evgen242/auto-inventory.git
fi
cd auto-inventory

# 3. Настройка окружения
echo -e "\n${YELLOW}3. Настройка окружения...${NC}"
if [ ! -f .env.docker ]; then
    cp .env.docker.example .env.docker
    # Генерируем случайный SECRET_KEY
    NEW_SECRET_KEY=$(openssl rand -base64 32)
    sed -i "s/change-this-to-your-secret-key/$NEW_SECRET_KEY/" .env.docker
    echo -e "${GREEN}✅ .env.docker создан с новым SECRET_KEY${NC}"
else
    echo -e "${GREEN}✅ .env.docker уже существует${NC}"
fi

# 4. Запуск Docker контейнеров
echo -e "\n${YELLOW}4. Запуск Docker контейнеров...${NC}"
docker compose -f docker-compose-dev.yml down 2>/dev/null || true
docker compose -f docker-compose-dev.yml up -d --build

# 5. Ожидание и проверка
echo -e "\n${YELLOW}5. Проверка здоровья...${NC}"
sleep 15

if curl -s http://localhost:5001/health | grep -q healthy; then
    echo -e "${GREEN}✅ Приложение успешно запущено!${NC}"
    echo -e "${GREEN}🌐 Доступно по адресу: http://$(hostname -I | awk '{print $1}'):5001${NC}"
else
    echo -e "${RED}❌ Ошибка запуска приложения${NC}"
    docker compose -f docker-compose-dev.yml logs --tail=30
    exit 1
fi

# 6. Вывод информации
echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}✅ Развертывание завершено успешно!${NC}"
echo -e "${GREEN}=====================================${NC}"
echo -e "📊 Статус контейнеров:"
docker compose -f docker-compose-dev.yml ps
echo -e "\n📝 Логи: docker compose -f docker-compose-dev.yml logs -f"
echo -e "\n🛑 Остановка: docker compose -f docker-compose-dev.yml down"
echo -e "\n🌐 URL: http://$(hostname -I | awk '{print $1}'):5001"
echo -e "\n📝 Первый зарегистрированный пользователь становится администратором!"
