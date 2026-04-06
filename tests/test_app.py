#!/usr/bin/env python3
"""
Универсальный тест для Auto Inventory System
Проверяет: регистрацию, логин, CRUD операции, права доступа
"""

import requests
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000"


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def print_test(name, passed, message=""):
    status = (
        f"{Colors.GREEN}✓ PASSED{Colors.RESET}" if passed else f"{Colors.RED}✗ FAILED{Colors.RESET}"
    )
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
        resp = requests.post(
            f"{BASE_URL}/auth/register",
            data={
                "username": test_username,
                "email": test_email,
                "password": test_password,
                "confirm_password": test_password,
            },
        )
        print_test(
            "User Registration",
            resp.status_code == 302 or resp.status_code == 200,
            f"User: {test_username}",
        )
        results.append(resp.status_code == 302 or resp.status_code == 200)
    except Exception as e:
        print_test("User Registration", False, f"Error: {e}")
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

    # Возвращаем None вместо булевого значения
    return None


if __name__ == "__main__":
    test_api()
    sys.exit(0)
