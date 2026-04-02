from datetime import datetime, timedelta
from app import db
from app.models.car import Car, CarBrand
from app.models.warehouse import Warehouse
from sqlalchemy import func

class Statistics:
    @staticmethod
    def get_dashboard_stats():
        """Основная статистика для дашборда"""
        total_cars = Car.query.count()
        total_brands = db.session.query(func.count(func.distinct(Car.brand_id))).scalar() or 0
        total_warehouses = Warehouse.query.count()
        total_quantity = db.session.query(func.sum(Car.quantity)).scalar() or 0
        total_value = db.session.query(func.sum(Car.price * Car.quantity)).scalar() or 0
        
        return {
            'total_cars': total_cars,
            'total_brands': total_brands,
            'total_warehouses': total_warehouses,
            'total_quantity': total_quantity,
            'total_value': total_value,
            'average_price': total_value / total_quantity if total_quantity > 0 else 0
        }
    
    @staticmethod
    def get_cars_by_brand():
        """Статистика по маркам"""
        results = db.session.query(
            Car.brand_id,
            func.count(Car.id).label('count'),
            func.sum(Car.quantity).label('quantity'),
            func.avg(Car.price).label('avg_price')
        ).group_by(Car.brand_id).all()
        
        brands_data = []
        for r in results:
            brand = CarBrand.query.get(r.brand_id)
            if brand:
                brands_data.append({
                    'brand_id': r.brand_id,
                    'brand_name': brand.name,
                    'count': r.count,
                    'quantity': r.quantity,
                    'avg_price': float(r.avg_price) if r.avg_price else 0
                })
        
        return sorted(brands_data, key=lambda x: x['quantity'], reverse=True)
    
    @staticmethod
    def get_cars_by_warehouse():
        """Статистика по складам"""
        results = db.session.query(
            Car.warehouse_id,
            func.count(Car.id).label('count'),
            func.sum(Car.quantity).label('quantity'),
            func.sum(Car.price * Car.quantity).label('value')
        ).group_by(Car.warehouse_id).all()
        
        warehouses_data = []
        for r in results:
            warehouse = Warehouse.query.get(r.warehouse_id)
            if warehouse:
                capacity_used = (r.quantity / warehouse.capacity * 100) if warehouse.capacity > 0 else 0
                warehouses_data.append({
                    'warehouse_id': r.warehouse_id,
                    'warehouse_name': warehouse.name,
                    'location': warehouse.location,
                    'count': r.count,
                    'quantity': r.quantity,
                    'value': float(r.value) if r.value else 0,
                    'capacity_used': capacity_used
                })
        
        return sorted(warehouses_data, key=lambda x: x['quantity'], reverse=True)
    
    @staticmethod
    def get_price_distribution():
        """Распределение цен"""
        price_ranges = [
            (0, 10000, 'До 10k'),
            (10000, 50000, '10k-50k'),
            (50000, 100000, '50k-100k'),
            (100000, 500000, '100k-500k'),
            (500000, 1000000, '500k-1M'),
            (1000000, 5000000, '1M-5M'),
            (5000000, float('inf'), '5M+')
        ]
        
        distribution = []
        for min_price, max_price, label in price_ranges:
            query = Car.query.filter(Car.price >= min_price)
            if max_price != float('inf'):
                query = query.filter(Car.price < max_price)
            
            count = query.count()
            quantity = db.session.query(func.sum(Car.quantity)).filter(
                Car.price >= min_price,
                Car.price < max_price if max_price != float('inf') else True
            ).scalar() or 0
            
            distribution.append({
                'range': label,
                'min': min_price,
                'max': max_price,
                'count': count,
                'quantity': quantity
            })
        
        return distribution
    
    @staticmethod
    def get_year_distribution():
        """Распределение по годам"""
        results = db.session.query(
            Car.year,
            func.count(Car.id).label('count'),
            func.sum(Car.quantity).label('quantity')
        ).filter(Car.year.isnot(None)).group_by(Car.year).order_by(Car.year.desc()).all()
        
        return [{'year': r.year, 'count': r.count, 'quantity': r.quantity} for r in results]
    
    @staticmethod
    def get_top_cars(limit=10):
        """Топ автомобилей по цене"""
        top_by_price = Car.query.order_by(Car.price.desc()).limit(limit).all()
        top_by_quantity = Car.query.order_by(Car.quantity.desc()).limit(limit).all()
        
        return {
            'top_by_price': [car.to_dict() for car in top_by_price],
            'top_by_quantity': [car.to_dict() for car in top_by_quantity]
        }
    
    @staticmethod
    def get_trends():
        """Тренды и аналитика"""
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        new_cars = Car.query.filter(Car.created_at >= thirty_days_ago).count()
        
        most_expensive = Car.query.order_by(Car.price.desc()).first()
        cheapest = Car.query.order_by(Car.price.asc()).first()
        
        return {
            'new_cars_last_30_days': new_cars,
            'total_inventory_value': db.session.query(func.sum(Car.price * Car.quantity)).scalar() or 0,
            'most_expensive_car': most_expensive.to_dict() if most_expensive else None,
            'cheapest_car': cheapest.to_dict() if cheapest else None
        }
