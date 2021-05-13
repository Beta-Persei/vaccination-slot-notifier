"""
Django settings for vaccination_slot_notifier project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG")))


ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(" ")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party
    "phonenumber_field",
    "crispy_forms",
    "constance",
    # Apps
    "subscribers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "vaccination_slot_notifier.urls"

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

WSGI_APPLICATION = "vaccination_slot_notifier.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "static/"
# Add these new lines
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Templates
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_ID")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")

# Custom Settings
DISTRICT_SLOT_ENDPOINT = (
    "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
)
PINCODE_SLOT_ENDPOINT = (
    "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
)

STATES_ENDPOINT = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
DISTRICTS_ENDPOINT = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/%s"


SITE_HOST_DOMAIN = os.environ.get("DOMAIN")

# Twilio Settings
TWILIO_ACCOUND_SID = os.environ.get("TWILIO_ACCOUND_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
TWILIO_MAX_SMS_SIZE = 1600

# Phone Number Field
PHONENUMBER_DEFAULT_REGION = "IN"

# Constance Settings
CONSTANCE_CONFIG = {
    "SMS_SERVICE_ACTIVE": (False, "Whether SMS service is active or not"),
    "SNIFFING_INTERVAL_SECONDS": (300, "Seconds between each sniffer iteration"),
    "MAIL_COOLDOWN_SECONDS": (1800, "Seconds before a new mail is sent to a user."),
    "MAX_DAILY_SMS_COUNT": (5, "Maximum number of sms in a day to a user."),
}
