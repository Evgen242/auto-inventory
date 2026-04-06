from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db
from app.models.user import User
import os
import requests

bp = Blueprint("auth", __name__, url_prefix="/auth")


def send_telegram_notification(message):
    """Отправка уведомления в Telegram"""
    try:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

        if bot_token and chat_id and bot_token != "your_bot_token_here":
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data, timeout=5)
            print(f"Telegram notification sent: {message[:50]}...")
    except Exception as e:
        print(f"Telegram notification error: {e}")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Пожалуйста, проверьте имя пользователя и пароль", "danger")
            return redirect(url_for("auth.login"))

        if not user.is_active:
            flash("Аккаунт деактивирован", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Уведомление о входе администратора
        if user.is_admin:
            send_telegram_notification(
                f"🔐 <b>Вход администратора</b>\n\n"
                f"👤 {user.username}\n"
                f"📧 {user.email}\n"
                f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
            )

        flash(f"Добро пожаловать, {user.username}!", "success")
        return redirect(url_for("main.index"))

    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Пароли не совпадают", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Имя пользователя уже занято", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email уже зарегистрирован", "danger")
            return redirect(url_for("auth.register"))

        user = User(username=username, email=email)
        user.set_password(password)

        # Первый пользователь становится админом
        is_first = User.query.count() == 0
        if is_first:
            user.is_admin = True

        db.session.add(user)
        db.session.commit()

        # Отправляем уведомление в Telegram о новой регистрации
        user_count = User.query.count()
        message = (
            f"🆕 <b>Новая регистрация!</b>\n\n"
            f"👤 <b>Пользователь:</b> {username}\n"
            f"📧 <b>Email:</b> {email}\n"
            f"👥 <b>Всего пользователей:</b> {user_count}\n"
            f"📅 <b>Дата:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
            f"🔐 <b>Админ:</b> {'Да' if user.is_admin else 'Нет'}"
        )
        send_telegram_notification(message)

        flash("Регистрация успешна! Теперь вы можете войти", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("auth.login"))


@bp.route("/api/me")
@login_required
def api_me():
    return jsonify(current_user.to_dict())


@bp.route("/api/users")
@login_required
def api_users():
    if not current_user.is_admin:
        return jsonify({"error": "Доступ запрещен"}), 403

    users = User.query.all()
    return jsonify([user.to_dict() for user in users])
