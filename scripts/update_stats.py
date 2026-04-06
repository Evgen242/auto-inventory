#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime

# Получаем статистику через localhost
try:
    response = requests.get("http://localhost:5000/api/stats", timeout=10)
    data = response.json()

    # Формируем блок статистики
    stats_block = f"""## 📊 Статистика системы ({datetime.now().strftime('%d.%m.%Y')})

- 🚗 **Автомобилей:** {data.get('total_cars', 0)} моделей
- 🏷️ **Марок:** {data.get('total_brands', 0)}
- 🏭 **Складов:** {data.get('total_warehouses', 0)}
- 📦 **Всего единиц:** {data.get('total_quantity', 0)}
- 💰 **Общая стоимость:** {data.get('total_value', 0):,.0f} ₽

### Распределение по складам:
"""
    for w in data.get("cars_by_warehouse", []):
        stats_block += f"- **{w['warehouse']}:** {w['quantity']} ед. ({w['count']} моделей)\n"

    print(stats_block)

    # Сохраняем в файл
    with open("/tmp/stats.md", "w", encoding="utf-8") as f:
        f.write(stats_block)

    print("✅ Stats saved")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
