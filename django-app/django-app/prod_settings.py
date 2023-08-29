# pylint: disable=wildcard-import,unused-wildcard-import
from .common_settings import *

DEBUG = False

ALLOWED_HOSTS = ["djangotest.fly.dev"]
CSRF_TRUSTED_ORIGINS = ["https://djangotest.fly.dev"]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 60
# SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
