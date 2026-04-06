from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def index():
    return render_template("index.html", user=current_user)


@bp.route("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "app": "Auto Inventory System",
            "version": "1.0.0",
        }
    )


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
