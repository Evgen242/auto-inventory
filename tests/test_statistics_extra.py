"""Дополнительные тесты для статистики"""
import pytest
from app import db
from app.models.car import Car, CarBrand
from app.models.warehouse import Warehouse
from app.models.statistics import Statistics


def test_statistics_class_exists():
    """Тест: класс Statistics существует"""
    assert Statistics is not None
    assert hasattr(Statistics, "get_dashboard_stats")


def test_get_dashboard_stats_returns_dict(app):
    """Тест: get_dashboard_stats возвращает словарь со статистикой"""
    with app.app_context():
        stats = Statistics.get_dashboard_stats()
        assert isinstance(stats, dict)
        # Проверяем ключи
        expected_keys = [
            "total_cars",
            "total_brands",
            "total_warehouses",
            "total_quantity",
            "total_value",
            "average_price",
        ]
        for key in expected_keys:
            assert key in stats
        # Проверяем типы значений
        assert isinstance(stats["total_cars"], int)
        assert isinstance(stats["total_brands"], int)
        assert isinstance(stats["total_warehouses"], int)


def test_get_dashboard_stats_with_data(app):
    """Тест: статистика с данными в БД"""
    with app.app_context():
        # Создаем тестовые данные
        brand = CarBrand(name="Stats Brand")
        warehouse = Warehouse(name="Stats Warehouse", location="Stats Location")
        db.session.add(brand)
        db.session.add(warehouse)
        db.session.commit()

        car = Car(
            brand_id=brand.id,
            warehouse_id=warehouse.id,
            model="Stats Car",
            year=2023,
            vin="STATSVIN123",
            price=25000,
            quantity=3,
        )
        db.session.add(car)
        db.session.commit()

        stats = Statistics.get_dashboard_stats()
        assert stats["total_cars"] >= 1
        assert stats["total_brands"] >= 1
        assert stats["total_warehouses"] >= 1
        assert stats["total_quantity"] >= 3
        assert stats["total_value"] >= 75000


def test_get_cars_by_brand_returns_list(app):
    """Тест: get_cars_by_brand возвращает список"""
    with app.app_context():
        result = Statistics.get_cars_by_brand()
        assert isinstance(result, list)


def test_get_cars_by_warehouse_returns_list(app):
    """Тест: get_cars_by_warehouse возвращает список"""
    with app.app_context():
        result = Statistics.get_cars_by_warehouse()
        assert isinstance(result, list)


def test_get_top_cars_returns_list(app):
    """Тест: get_top_cars возвращает список (исправлено с get_popular_cars)"""
    with app.app_context():
        result = Statistics.get_top_cars()
        assert isinstance(result, list)


def test_get_recent_cars_returns_list(app):
    """Тест: get_recent_cars возвращает список"""
    with app.app_context():
        result = Statistics.get_recent_cars()
        assert isinstance(result, list)


def test_dashboard_stats_integration(authenticated_client, app):
    """Тест: интеграция статистики с дашбордом"""
    with app.app_context():
        # Создаем тестовые данные
        brand = CarBrand(name="Integration Brand")
        warehouse = Warehouse(name="Integration Warehouse", location="Integration")
        db.session.add(brand)
        db.session.add(warehouse)
        db.session.commit()

        car = Car(
            brand_id=brand.id,
            warehouse_id=warehouse.id,
            model="Integration Car",
            year=2023,
            vin="INTVIN123",
            price=40000,
            quantity=2,
        )
        db.session.add(car)
        db.session.commit()

        stats = Statistics.get_dashboard_stats()
        assert stats["total_cars"] > 0

        response = authenticated_client.get("/dashboard")
        assert response.status_code == 200
        content = response.data.decode("utf-8")
        # Проверяем что статистика отображается
        assert str(stats["total_cars"]) in content or "car" in content.lower()


def test_statistics_methods_exist():
    """Тест: проверка наличия всех методов статистики (исправлено)"""
    methods = [
        "get_dashboard_stats",
        "get_cars_by_brand",
        "get_cars_by_warehouse",
        "get_top_cars",
        "get_recent_cars",
    ]
    for method in methods:
        assert hasattr(Statistics, method), f"Method {method} not found"
