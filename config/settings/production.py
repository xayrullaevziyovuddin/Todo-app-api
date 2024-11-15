from .base import *  # noqa

ALLOWED_HOSTS = [
    "yourusername.pythonanywhere.com",  # Ваше имя пользователя на PythonAnywhere
    "api.example.com",  # Дополнительные домены, если есть
    "admin.example.com",  # Дополнительные домены, если есть
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = ["https://api.example.com", "https://admin.example.com"]
CORS_ALLOWED_ORIGINS = ["https://api.example.com", "https://admin.example.com"]

DEBUG = False

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = False
CORS_ORIGIN_ALLOW_ALL = False
