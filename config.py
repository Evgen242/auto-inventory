import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'dev-secret-key-change-in-production'
    
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://deploy:deploy_password_2026@localhost/auto_inventory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True
    
    APP_NAME = 'Auto Inventory System'
    APP_VERSION = '1.0.0'
