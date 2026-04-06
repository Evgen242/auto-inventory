from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from app.models.statistics import Statistics

bp = Blueprint("statistics", __name__, url_prefix="/stats")


@bp.route("/dashboard")
@login_required
def dashboard():
    """Страница статистики"""
    return render_template("statistics.html", user=current_user)


@bp.route("/api/dashboard")
@login_required
def api_dashboard():
    """API для дашборда"""
    try:
        data = {
            "overview": Statistics.get_dashboard_stats(),
            "by_brand": Statistics.get_cars_by_brand(),
            "by_warehouse": Statistics.get_cars_by_warehouse(),
            "price_distribution": [],
            "year_distribution": Statistics.get_year_distribution(),
            "top_cars": Statistics.get_top_cars(5),
            "trends": Statistics.get_trends(),
        }

        # Обрабатываем price_distribution отдельно, заменяя Infinity на null
        price_dist = Statistics.get_price_distribution()
        for item in price_dist:
            # Заменяем Infinity на None для JSON
            if item["max"] == float("inf"):
                item["max"] = None
            data["price_distribution"].append(item)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/api/brand/<int:brand_id>")
@login_required
def brand_stats(brand_id):
    """Детальная статистика по марке"""
    from app.models.car import CarBrand

    brand = CarBrand.query.get_or_404(brand_id)

    stats = {
        "brand": brand.to_dict(),
        "cars": [car.to_dict() for car in brand.cars],
        "total_quantity": sum(car.quantity for car in brand.cars),
        "total_value": sum(car.price * car.quantity for car in brand.cars),
        "average_price": sum(car.price * car.quantity for car in brand.cars)
        / sum(car.quantity for car in brand.cars)
        if brand.cars
        else 0,
    }

    return jsonify(stats)


@bp.route("/api/warehouse/<int:warehouse_id>")
@login_required
def warehouse_stats(warehouse_id):
    """Детальная статистика по складу"""
    from app.models.warehouse import Warehouse

    warehouse = Warehouse.query.get_or_404(warehouse_id)

    stats = {
        "warehouse": warehouse.to_dict(),
        "cars": [car.to_dict() for car in warehouse.cars],
        "total_quantity": sum(car.quantity for car in warehouse.cars),
        "total_value": sum(car.price * car.quantity for car in warehouse.cars),
        "occupancy_rate": (sum(car.quantity for car in warehouse.cars) / warehouse.capacity * 100)
        if warehouse.capacity > 0
        else 0,
    }

    return jsonify(stats)
