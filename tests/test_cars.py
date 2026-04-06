"""Тесты для автомобилей"""
import pytest
from app import db
from app.models.car import Car, CarBrand
from app.models.warehouse import Warehouse


def test_create_car(authenticated_client, app):
    """Тест создания автомобиля"""
    with app.app_context():
        brand = CarBrand(name="Toyota")
        warehouse = Warehouse(name="Main Warehouse", location="City Center")
        db.session.add(brand)
        db.session.add(warehouse)
        db.session.commit()

        response = authenticated_client.post(
            "/api/cars",
            json={
                "brand_id": brand.id,
                "warehouse_id": warehouse.id,
                "model": "Camry",
                "year": 2023,
                "vin": "TESTVIN123456",
                "price": 35000,
                "quantity": 5,
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert "id" in data


def test_delete_car(admin_client, app):
    """Тест удаления автомобиля (только админ)"""
    with app.app_context():
        brand = CarBrand(name="Honda")
        warehouse = Warehouse(name="East Warehouse", location="East Side")
        db.session.add(brand)
        db.session.add(warehouse)
        db.session.commit()

        car = Car(
            brand_id=brand.id,
            warehouse_id=warehouse.id,
            model="Accord",
            year=2023,
            vin="TESTVIN789012",
            price=30000,
            quantity=3,
        )
        db.session.add(car)
        db.session.commit()
        car_id = car.id

        # Удаляем автомобиль (админ)
        response = admin_client.delete(f"/api/cars/{car_id}")
        assert response.status_code == 200

        # Проверяем что автомобиль удален
        deleted_car = db.session.get(Car, car_id)
        assert deleted_car is None


def test_get_cars_list(authenticated_client):
    """Тест получения списка автомобилей (пагинация)"""
    response = authenticated_client.get("/api/cars")
    assert response.status_code == 200
    data = response.get_json()
    # API возвращает пагинированный ответ
    assert "items" in data or isinstance(data, list)
    if "items" in data:
        assert isinstance(data["items"], list)
    else:
        assert isinstance(data, list)


def test_get_car_by_id(authenticated_client, app):
    """Тест получения конкретного автомобиля"""
    with app.app_context():
        brand = CarBrand(name="BMW")
        warehouse = Warehouse(name="West Warehouse", location="West Side")
        db.session.add(brand)
        db.session.add(warehouse)
        db.session.commit()

        car = Car(
            brand_id=brand.id,
            warehouse_id=warehouse.id,
            model="X5",
            year=2023,
            vin="TESTVIN345678",
            price=60000,
            quantity=2,
        )
        db.session.add(car)
        db.session.commit()

        response = authenticated_client.get(f"/api/cars/{car.id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["model"] == "X5"


def test_update_car(admin_client, app):
    """Тест обновления автомобиля (только админ)"""
    with app.app_context():
        brand = CarBrand(name="Mercedes")
        warehouse = Warehouse(name="North Warehouse", location="North Side")
        db.session.add(brand)
        db.session.add(warehouse)
        db.session.commit()

        car = Car(
            brand_id=brand.id,
            warehouse_id=warehouse.id,
            model="E-Class",
            year=2022,
            vin="TESTVIN901234",
            price=55000,
            quantity=1,
        )
        db.session.add(car)
        db.session.commit()

        response = admin_client.put(f"/api/cars/{car.id}", json={"price": 58000, "quantity": 2})
        assert response.status_code == 200

        updated_car = db.session.get(Car, car.id)
        assert updated_car.price == 58000
        assert updated_car.quantity == 2


def test_search_cars(authenticated_client, app):
    """Тест поиска автомобилей"""
    with app.app_context():
        brand = CarBrand(name="Audi")
        warehouse = Warehouse(name="South Warehouse", location="South Side")
        db.session.add(brand)
        db.session.add(warehouse)
        db.session.commit()

        car = Car(
            brand_id=brand.id,
            warehouse_id=warehouse.id,
            model="A4",
            year=2023,
            vin="TESTVIN567890",
            price=45000,
            quantity=4,
        )
        db.session.add(car)
        db.session.commit()

        response = authenticated_client.get("/api/cars?search=A4")
        assert response.status_code == 200
        data = response.get_json()
        # Может быть пагинация или список
        if "items" in data:
            assert len(data["items"]) > 0
        else:
            assert len(data) > 0


def test_cars_api_unauthorized(client):
    """Тест: неавторизованный доступ к API автомобилей (редирект на логин)"""
    response = client.get("/api/cars")
    # API требует авторизации, редирект на логин
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_cars_api_unauthorized_post(client):
    """Тест: неавторизованный не может создать автомобиль"""
    response = client.post("/api/cars", json={"brand_id": 1, "model": "Test", "year": 2023})
    # Редирект на страницу логина
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_regular_user_cannot_delete(authenticated_client, app):
    """Тест: обычный пользователь не может удалить автомобиль"""
    with app.app_context():
        brand = CarBrand(name="Test Brand")
        warehouse = Warehouse(name="Test Warehouse", location="Test")
        db.session.add(brand)
        db.session.add(warehouse)
        db.session.commit()

        car = Car(
            brand_id=brand.id,
            warehouse_id=warehouse.id,
            model="Test Car",
            year=2023,
            vin="TESTVIN999999",
            price=10000,
            quantity=1,
        )
        db.session.add(car)
        db.session.commit()
        car_id = car.id

        # Обычный пользователь пытается удалить
        response = authenticated_client.delete(f"/api/cars/{car_id}")
        # Должен быть запрет (403)
        assert response.status_code == 403


def test_regular_user_cannot_update(authenticated_client, app):
    """Тест: обычный пользователь не может обновить автомобиль"""
    with app.app_context():
        brand = CarBrand(name="Test Brand 2")
        warehouse = Warehouse(name="Test Warehouse 2", location="Test 2")
        db.session.add(brand)
        db.session.add(warehouse)
        db.session.commit()

        car = Car(
            brand_id=brand.id,
            warehouse_id=warehouse.id,
            model="Test Car 2",
            year=2023,
            vin="TESTVIN888888",
            price=20000,
            quantity=2,
        )
        db.session.add(car)
        db.session.commit()

        # Обычный пользователь пытается обновить
        response = authenticated_client.put(f"/api/cars/{car.id}", json={"price": 25000})
        # Должен быть запрет (403)
        assert response.status_code == 403
