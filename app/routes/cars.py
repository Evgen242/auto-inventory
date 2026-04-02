from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models.car import CarBrand, Car
from app.models.warehouse import Warehouse

bp = Blueprint('cars', __name__, url_prefix='/api')

@bp.route('/brands', methods=['GET', 'POST'])
@login_required
def handle_brands():
    if request.method == 'POST':
        if not current_user.is_admin:
            return jsonify({'error': 'Доступ запрещен'}), 403
        
        data = request.json
        if not data.get('name'):
            return jsonify({'error': 'Название марки обязательно'}), 400
        
        if CarBrand.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Марка уже существует'}), 400
        
        brand = CarBrand(name=data['name'])
        db.session.add(brand)
        db.session.commit()
        return jsonify(brand.to_dict()), 201
    
    brands = CarBrand.query.order_by(CarBrand.name).all()
    return jsonify([brand.to_dict() for brand in brands])

@bp.route('/brands/<int:id>', methods=['DELETE'])
@login_required
def delete_brand(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    brand = CarBrand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    return jsonify({'message': 'Марка удалена'}), 200

@bp.route('/warehouses', methods=['GET', 'POST'])
@login_required
def handle_warehouses():
    if request.method == 'POST':
        if not current_user.is_admin:
            return jsonify({'error': 'Доступ запрещен'}), 403
        
        data = request.json
        if not data.get('name') or not data.get('location'):
            return jsonify({'error': 'Название и местоположение обязательны'}), 400
        
        warehouse = Warehouse(
            name=data['name'],
            location=data['location'],
            capacity=data.get('capacity', 100)
        )
        db.session.add(warehouse)
        db.session.commit()
        return jsonify(warehouse.to_dict()), 201
    
    warehouses = Warehouse.query.order_by(Warehouse.name).all()
    return jsonify([warehouse.to_dict() for warehouse in warehouses])

@bp.route('/warehouses/<int:id>', methods=['DELETE', 'PUT'])
@login_required
def manage_warehouse(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    warehouse = Warehouse.query.get_or_404(id)
    
    if request.method == 'DELETE':
        db.session.delete(warehouse)
        db.session.commit()
        return jsonify({'message': 'Склад удален'}), 200
    
    if request.method == 'PUT':
        data = request.json
        warehouse.name = data.get('name', warehouse.name)
        warehouse.location = data.get('location', warehouse.location)
        warehouse.capacity = data.get('capacity', warehouse.capacity)
        db.session.commit()
        return jsonify(warehouse.to_dict()), 200

@bp.route('/cars', methods=['GET', 'POST'])
@login_required
def handle_cars():
    if request.method == 'POST':
        data = request.json
        
        required_fields = ['model', 'brand_id', 'warehouse_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Поле {field} обязательно'}), 400
        
        car = Car(
            model=data['model'],
            year=data.get('year'),
            vin=data.get('vin'),
            quantity=data.get('quantity', 1),
            price=data.get('price', 0),
            description=data.get('description'),
            brand_id=data['brand_id'],
            warehouse_id=data['warehouse_id']
        )
        
        db.session.add(car)
        db.session.commit()
        return jsonify(car.to_dict()), 201
    
    # GET - получаем параметры поиска и фильтрации
    query = Car.query
    
    # Поиск по тексту (модель, VIN, марка)
    search = request.args.get('search', '').strip()
    if search:
        # Ищем по модели, VIN и названию марки
        query = query.join(CarBrand).filter(
            or_(
                Car.model.ilike(f'%{search}%'),
                Car.vin.ilike(f'%{search}%'),
                CarBrand.name.ilike(f'%{search}%')
            )
        )
    
    # Фильтр по марке
    brand_id = request.args.get('brand_id')
    if brand_id and brand_id != 'all':
        query = query.filter_by(brand_id=brand_id)
    
    # Фильтр по складу
    warehouse_id = request.args.get('warehouse_id')
    if warehouse_id and warehouse_id != 'all':
        query = query.filter_by(warehouse_id=warehouse_id)
    
    # Фильтр по году
    year_from = request.args.get('year_from')
    if year_from:
        query = query.filter(Car.year >= int(year_from))
    
    year_to = request.args.get('year_to')
    if year_to:
        query = query.filter(Car.year <= int(year_to))
    
    # Фильтр по цене
    price_from = request.args.get('price_from')
    if price_from:
        query = query.filter(Car.price >= float(price_from))
    
    price_to = request.args.get('price_to')
    if price_to:
        query = query.filter(Car.price <= float(price_to))
    
    # Сортировка
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    if sort_order == 'desc':
        query = query.order_by(getattr(Car, sort_by).desc())
    else:
        query = query.order_by(getattr(Car, sort_by).asc())
    
    # Пагинация
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [car.to_dict() for car in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@bp.route('/cars/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def manage_car(id):
    car = Car.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(car.to_dict())
    
    if request.method == 'PUT':
        if not current_user.is_admin:
            return jsonify({'error': 'Доступ запрещен'}), 403
        
        data = request.json
        car.model = data.get('model', car.model)
        car.year = data.get('year', car.year)
        car.vin = data.get('vin', car.vin)
        car.quantity = data.get('quantity', car.quantity)
        car.price = data.get('price', car.price)
        car.description = data.get('description', car.description)
        car.brand_id = data.get('brand_id', car.brand_id)
        car.warehouse_id = data.get('warehouse_id', car.warehouse_id)
        
        db.session.commit()
        return jsonify(car.to_dict()), 200
    
    if request.method == 'DELETE':
        if not current_user.is_admin:
            return jsonify({'error': 'Доступ запрещен'}), 403
        
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'Автомобиль удален'}), 200

@bp.route('/stats')
@login_required
def get_stats():
    total_cars = Car.query.count()
    total_brands = CarBrand.query.count()
    total_warehouses = Warehouse.query.count()
    total_quantity = db.session.query(db.func.sum(Car.quantity)).scalar() or 0
    
    cars_by_warehouse = db.session.query(
        Warehouse.name,
        db.func.count(Car.id).label('count'),
        db.func.sum(Car.quantity).label('quantity')
    ).outerjoin(Car).group_by(Warehouse.id).all()
    
    return jsonify({
        'total_cars': total_cars,
        'total_brands': total_brands,
        'total_warehouses': total_warehouses,
        'total_quantity': total_quantity,
        'cars_by_warehouse': [
            {
                'warehouse': w[0],
                'count': w[1],
                'quantity': w[2] or 0
            } for w in cars_by_warehouse
        ]
    })
