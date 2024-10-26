from .base import *  # noqa

ALLOWED_HOSTS = ["*"]
DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]

# Добавьте debug_toolbar только если его еще нет
if "debug_toolbar" not in INSTALLED_APPS:
    INSTALLED_APPS.append("debug_toolbar")  # noqa: F405

# Добавьте DebugToolbarMiddleware только если его еще нет
if "debug_toolbar.middleware.DebugToolbarMiddleware" not in MIDDLEWARE:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
