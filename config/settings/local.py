from .base import *


DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["debug_toolbar"]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Django DEBUG Toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]
