from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db
from app.models.user import User
import os
import requests
import sys

bp = Blueprint('auth', __name__, url_prefix='/auth')

def send_telegram_notification(message):
    try:
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
        if bot_token and chat_id:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
            requests.post(url, data=data, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")

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
        
        flash(f'Добро пожаловать, {user.username}!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    print("=== REGISTER START ===", flush=True)
    
    if current_user.is_authenticated:
        print("User already authenticated", flush=True)
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        print("POST request received", flush=True)
        
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        print(f"Username: {username}, Email: {email}", flush=True)
        
        if password != confirm_password:
            print("Password mismatch", flush=True)
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            print(f"Username {username} already exists", flush=True)
            flash('Имя пользователя уже занято', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            print(f"Email {email} already exists", flush=True)
            flash('Email уже зарегистрирован', 'danger')
            return redirect(url_for('auth.register'))
        
        print("Creating user...", flush=True)
        user = User(username=username, email=email)
        user.set_password(password)
        
        if User.query.count() == 0:
            user.is_admin = True
        
        db.session.add(user)
        print("User added to session", flush=True)
        
        db.session.commit()
        print("User committed to DB", flush=True)
        
        user_count = User.query.count()
        message = f"New registration: {username} ({email})"
        send_telegram_notification(message)
        
        flash('Регистрация успешна! Теперь вы можете войти', 'success')
        return redirect(url_for('auth.login'))
    
    print("GET request received", flush=True)
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
