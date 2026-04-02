#!/usr/bin/env python3
"""
Универсальный тест для Auto Inventory System
Проверяет: регистрацию, логин, CRUD операции, права доступа
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000"
# BASE_URL = "https://autolot25.ddns.net:8086"  # Для теста через HTTPS

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(name, passed, message=""):
    status = f"{Colors.GREEN}✓ PASSED{Colors.RESET}" if passed else f"{Colors.RED}✗ FAILED{Colors.RESET}"
    print(f"[{status}] {name}")
    if message:
        print(f"      {message}")

def test_api():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}Auto Inventory System - Universal Test{Colors.RESET}")
    print(f"{Colors.BLUE}Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    results = []
    
    # 1. Health check
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        print_test("Health Check", resp.status_code == 200, f"Status: {resp.status_code}")
        results.append(resp.status_code == 200)
    except Exception as e:
        print_test("Health Check", False, f"Error: {e}")
        results.append(False)
    
    # 2. Регистрация нового пользователя
    test_username = f"testuser_{datetime.now().strftime('%H%M%S')}"
    test_email = f"{test_username}@example.com"
    test_password = "testpass123"
    
    try:
        resp = requests.post(f"{BASE_URL}/auth/register", data={
            'username': test_username,
            'email': test_email,
            'password': test_password,
            'confirm_password': test_password
        })
        print_test("User Registration", resp.status_code == 302 or resp.status_code == 200, 
                   f"User: {test_username}")
        results.append(resp.status_code == 302 or resp.status_code == 200)
    except Exception as e:
        print_test("User Registration", False, f"Error: {e}")
        results.append(False)
    
    # 3. Логин
    session = requests.Session()
    try:
        resp = session.post(f"{BASE_URL}/auth/login", data={
            'username': test_username,
            'password': test_password
        })
        print_test("User Login", resp.status_code == 302 or resp.status_code == 200, 
                   f"User: {test_username}")
        results.append(resp.status_code == 302 or resp.status_code == 200)
    except Exception as e:
        print_test("User Login", False, f"Error: {e}")
        results.append(False)
    
    # 4. Получение списка автомобилей
    try:
        resp = session.get(f"{BASE_URL}/api/cars")
        print_test("Get Cars List", resp.status_code == 200, f"Status: {resp.status_code}")
        results.append(resp.status_code == 200)
        if resp.status_code == 200:
            cars = resp.json()
            print(f"      Total cars: {len(cars) if isinstance(cars, list) else cars.get('total', 0)}")
    except Exception as e:
        print_test("Get Cars List", False, f"Error: {e}")
        results.append(False)
    
    # 5. Добавление автомобиля
    car_data = {
        'model': f'Test Car {datetime.now().strftime("%H%M%S")}',
        'year': 2024,
        'vin': f'TEST{datetime.now().strftime("%H%M%S")}',
        'quantity': 2,
        'price': 500000,
        'brand_id': 1,
        'warehouse_id': 1
    }
    try:
        resp = session.post(f"{BASE_URL}/api/cars", json=car_data)
        print_test("Add Car", resp.status_code == 201, f"Model: {car_data['model']}")
        results.append(resp.status_code == 201)
        car_id = resp.json().get('id') if resp.status_code == 201 else None
    except Exception as e:
        print_test("Add Car", False, f"Error: {e}")
        results.append(False)
        car_id = None
    
    # 6. Получение статистики
    try:
        resp = session.get(f"{BASE_URL}/api/stats")
        print_test("Get Statistics", resp.status_code == 200, f"Status: {resp.status_code}")
        results.append(resp.status_code == 200)
        if resp.status_code == 200:
            stats = resp.json()
            print(f"      Total cars: {stats.get('total_cars', 0)}")
    except Exception as e:
        print_test("Get Statistics", False, f"Error: {e}")
        results.append(False)
    
    # 7. Удаление добавленного автомобиля (только если был создан)
    if car_id:
        try:
            resp = session.delete(f"{BASE_URL}/api/cars/{car_id}")
            print_test("Delete Own Car", resp.status_code == 200, f"Car ID: {car_id}")
            results.append(resp.status_code == 200)
        except Exception as e:
            print_test("Delete Own Car", False, f"Error: {e}")
            results.append(False)
    else:
        print_test("Delete Own Car", False, "Car not created")
        results.append(False)
    
    # 8. Проверка демо-пользователя (только чтение)
    demo_session = requests.Session()
    try:
        resp = demo_session.post(f"{BASE_URL}/auth/login", data={
            'username': 'demo',
            'password': 'demo123'
        })
        print_test("Demo Login", resp.status_code == 302 or resp.status_code == 200)
        results.append(resp.status_code == 302 or resp.status_code == 200)
        
        # Демо не должен добавлять авто
        resp = demo_session.post(f"{BASE_URL}/api/cars", json=car_data)
        can_add = resp.status_code == 403
        print_test("Demo Cannot Add Car", can_add, f"Status: {resp.status_code} (expected 403)")
        results.append(can_add)
    except Exception as e:
        print_test("Demo Login", False, f"Error: {e}")
        results.append(False)
    
    # 9. Поиск автомобилей
    try:
        resp = session.get(f"{BASE_URL}/api/cars?search=Toyota")
        print_test("Search Cars", resp.status_code == 200, f"Status: {resp.status_code}")
        results.append(resp.status_code == 200)
    except Exception as e:
        print_test("Search Cars", False, f"Error: {e}")
        results.append(False)
    
    # 10. Фильтрация по цене
    try:
        resp = session.get(f"{BASE_URL}/api/cars?price_from=1000000&price_to=5000000")
        print_test("Price Filter", resp.status_code == 200, f"Status: {resp.status_code}")
        results.append(resp.status_code == 200)
    except Exception as e:
        print_test("Price Filter", False, f"Error: {e}")
        results.append(False)
    
    # Итоги
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    passed = sum(results)
    total = len(results)
    print(f"{Colors.BLUE}RESULTS: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"{Colors.GREEN}✓ ALL TESTS PASSED! Application is working correctly.{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠ Some tests failed. Please check the application.{Colors.RESET}")
    
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    return passed == total

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
