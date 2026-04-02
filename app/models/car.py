from datetime import datetime
from app import db

class CarBrand(db.Model):
    __tablename__ = 'car_brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cars = db.relationship('Car', backref='brand', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    vin = db.Column(db.String(17), unique=True)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text)
    brand_id = db.Column(db.Integer, db.ForeignKey('car_brands.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # Кто добавил автомобиль

    def to_dict(self):
        return {
            'id': self.id,
            'model': self.model,
            'year': self.year,
            'vin': self.vin,
            'quantity': self.quantity,
            'price': self.price,
            'description': self.description,
            'brand': self.brand.name if self.brand else None,
            'brand_id': self.brand_id,
            'warehouse': self.warehouse.name if self.warehouse else None,
            'warehouse_id': self.warehouse_id,
            'location': self.warehouse.location if self.warehouse else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by
        }
