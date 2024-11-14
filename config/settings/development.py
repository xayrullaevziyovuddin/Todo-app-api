from .base import *  # noqa

ALLOWED_HOSTS = ["*"]
DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]

# Добавьте debug_toolbar, если его еще нет в INSTALLED_APPS
if "debug_toolbar" not in INSTALLED_APPS:
    INSTALLED_APPS.append("debug_toolbar")  # noqa: F405

# Добавьте DebugToolbarMiddleware, если его еще нет в MIDDLEWARE
if "debug_toolbar.middleware.DebugToolbarMiddleware" not in MIDDLEWARE:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

# Настройки CORS
# Добавьте 'corsheaders' в INSTALLED_APPS, если его там еще нет
if "corsheaders" not in INSTALLED_APPS:
    INSTALLED_APPS.append("corsheaders")

# Добавьте CorsMiddleware в начало списка MIDDLEWARE, если его там еще нет
if "corsheaders.middleware.CorsMiddleware" not in MIDDLEWARE:
    MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

# Разрешить запросы от всех источников (только для разработки)
CORS_ALLOW_ALL_ORIGINS = True
