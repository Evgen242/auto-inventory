#!/bin/bash

echo "=== GitHub Actions Status Check ==="
echo ""

echo "📊 Last commit:"
git log -1 --oneline

echo ""
echo "🔗 Check GitHub Actions:"
echo "https://github.com/Evgen242/auto-inventory/actions"

echo ""
echo "🖥️ Local server status:"
sudo systemctl status auto-inventory --no-pager | head -5

echo ""
echo "🏥 Health check:"
curl -s -k https://autolot25.ddns.net:8086/health | python3 -m json.tool 2>/dev/null || echo "❌ Not responding"

echo ""
echo "🐳 Docker status:"
docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null || echo "Docker not running"

echo ""
echo "💾 Last backup:"
ls -lh /var/backups/auto-inventory/ 2>/dev/null | tail -3 || echo "No backups found"
