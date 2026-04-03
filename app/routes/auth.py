from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db
from app.models.user import User
import os
import requests

bp = Blueprint('auth', __name__, url_prefix='/auth')

def send_telegram_notification(message):
    print("=== TELEGRAM FUNCTION CALLED ===", flush=True)
    print(f"Message: {message[:100]}", flush=True)
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
    
    print(f"Token: {bot_token[:20]}...", flush=True)
    print(f"Chat ID: {chat_id}", flush=True)
    
    if bot_token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
            response = requests.post(url, data=data, timeout=5)
            print(f"Response status: {response.status_code}", flush=True)
            print(f"Response: {response.text[:200]}", flush=True)
        except Exception as e:
            print(f"Error: {e}", flush=True)
    else:
        print("Token or chat_id missing!", flush=True)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash('Пожалуйста, проверьте имя пользователя и пароль', 'danger')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('Аккаунт деактивирован', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        user.last_login = datetime.utcnow()
        db.session.commit()

        if user.is_admin:
            msg = f"🔐 Admin login: {user.username} ({user.email})"
            send_telegram_notification(msg)

        flash(f'Добро пожаловать, {user.username}!', 'success')
        return redirect(url_for('main.index'))

    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Имя пользователя уже занято', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Email уже зарегистрирован', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(password)

        if User.query.count() == 0:
            user.is_admin = True

        db.session.add(user)
        db.session.commit()

        user_count = User.query.count()
        msg = f"🆕 New registration: {username} ({email})\nTotal users: {user_count}"
        send_telegram_notification(msg)

        flash('Регистрация успешна! Теперь вы можете войти', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/api/me')
@login_required
def api_me():
    return jsonify(current_user.to_dict())

@bp.route('/api/users')
@login_required
def api_users():
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])
