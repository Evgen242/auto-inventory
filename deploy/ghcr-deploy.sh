#!/bin/bash
# Деплой из GitHub Container Registry

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Deploying from GitHub Container Registry...${NC}"

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker не установлен. Устанавливаем...${NC}"
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
fi

# Создание .env файла
if [ ! -f config/.env.ghcr ]; then
    echo -e "${YELLOW}Создаем config/.env.ghcr...${NC}"
    cat > config/.env.ghcr << 'ENVEOF'
DB_PASSWORD=$(openssl rand -base64 16)
SECRET_KEY=$(openssl rand -base64 32)
ENVEOF
    echo -e "${GREEN}✅ config/.env.ghcr создан${NC}"
fi

# Загрузка переменных
export $(grep -v '^#' config/.env.ghcr | xargs)

# Pull образа из GHCR
echo -e "${YELLOW}Pulling image from GHCR...${NC}"
docker pull ghcr.io/evgen242/auto-inventory:latest

# Запуск
echo -e "${YELLOW}Starting containers...${NC}"
docker compose -f docker-compose.ghcr.yml up -d

# Проверка
sleep 10
if curl -s http://localhost:5000/health | grep -q healthy; then
    echo -e "${GREEN}✅ Deployed successfully!${NC}"
    echo -e "${GREEN}🌐 App is running at: http://localhost:5000${NC}"
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    docker compose -f docker-compose.ghcr.yml logs
    exit 1
fi
