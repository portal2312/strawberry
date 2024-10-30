"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-rz5*e!r+dnj+y#*++s=4g$uw#of85o+^n_-z7mi#_@47#euh!i",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # channels Installation: MUST first line.
    # https://channels.readthedocs.io/en/latest/installation.html
    # FIXME: Not display the debug_toolbar toolbar for Daphne.
    "daphne",
    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # django-debug-toolbar: Install the App.
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#install-the-app
    "debug_toolbar",
    # strawberry-graphql: Integrations/Django/Async Django.
    # https://strawberry.rocks/docs/integrations/django#async-django
    "strawberry_django",
    # Local apps.
    "utils",
    "app",
    "my_pydantic",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Support django-debug-toolbar at strawberry-graphql-django.
    # https://strawberry-graphql.github.io/strawberry-django/integrations/debug-toolbar/
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # FIXME: runserver error.
    # "strawberry_django.middlewares.debug_toolbar.DebugToolbarMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type.
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# channels Installation.
# https://channels.readthedocs.io/en/latest/installation.html
ASGI_APPLICATION = "project.asgi.application"

# django-debug-toolbar: Configure Internal IPs.
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips
INTERNAL_IPS = [
    "127.0.0.1",
]

# The absolute path to the directory where collectstatic will collect static files for deployment.
# https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-STATIC_ROOT
STATIC_ROOT = BASE_DIR / "staticfiles"

# https://strawberry-graphql.github.io/strawberry-django/guide/settings/#strawberry_django
STRAWBERRY_DJANGO = {
    "FIELD_DESCRIPTION_FROM_HELP_TEXT": True,
    "TYPE_DESCRIPTION_FROM_MODEL_DOCSTRING": True,
}
