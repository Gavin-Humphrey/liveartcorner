"""
Django settings for liveartcorner project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
from decouple import config
from liveartcornerEmailApp.backends.email_backend import EmailBackend
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration 

import dj_database_url
from dotenv import load_dotenv

from liveartcorner.storage import CloudinaryMediaStorage
import cloudinary
import cloudinary_storage



load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default=get_random_secret_key())

DJANGO_SETTINGS_MODULE = config('DJANGO_SETTINGS_MODULE', default='liveartcorner.settings')



# SECURITY WARNING: don't run with debug turned on in production!
DOCKERIZED = config('DOCKERIZED', default=False, cast=bool)

DEBUG = config('DEBUG', default=False, cast=bool) if not DOCKERIZED else False

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default="", cast=lambda v: [s.strip() for s in v.split(",")]
)

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "base.apps.BaseConfig",
    "user.apps.UserConfig",
    "dashboard.apps.DashboardConfig",
    "item.apps.ItemConfig",    
    "cart.apps.CartConfig",
    "order.apps.OrderConfig",
    "wishlist.apps.WishlistConfig",
    "services.apps.ServicesConfig",
]

AUTH_USER_MODEL = 'user.User'


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "liveartcorner.urls"

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
                 "liveartcorner.context_processors.website_email",
            ],
        },
    },
]

WSGI_APPLICATION = "liveartcorner.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


if DEBUG:
    # Development settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Production settings
    DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') ####

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

#STATIC_ROOT = None


# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configure Cloudinary using the CLOUDINARY_URL environment variable
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME", "default_value"),
    api_key=config("CLOUDINARY_API_KEY", "default_value"),
    api_secret=config("CLOUDINARY_API_SECRET", "default_value"),
)

#if "CI" in os.environ or DEBUG:
if DEBUG:
    # Use Django's built-in static file serving during development
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

    # Use local filesystem storage for testing
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
else:
    # Use whitenoise for serving static files in production
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
    #STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

    # Use custom Cloudinary storage for user-uploaded files
    DEFAULT_FILE_STORAGE = "liveartcorner.storage.CloudinaryMediaStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


sentry_dsn = config("LIVEARTCORNER_SENTRY_DSN", default=None)

sentry_sdk.init(
    dsn=sentry_dsn,
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)


LOGIN_REDIRECT_URL = "/base/thank_you.html"


EMAIL_BACKEND = "liveartcornerEmailApp.backends.email_backend.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_FROM = config("WEBSITE_EMAIL", default="backup@example.com")
EMAIL_HOST_USER = config("WEBSITE_EMAIL", default="backup@example.com")
EMAIL_HOST_PASSWORD = config("WEBSITE_EMAIL_PASSWORD", default="Backuppassword")

PASSWORD_RESET_TIMEOUT = 15000



STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET")

BACKEND_DOMAIN = config("BACKEND_DOMAIN")
PAYMENT_SUCCESS_URL = config("PAYMENT_SUCCESS_URL")
PAYMENT_CANCEL_URL = config("PAYMENT_CANCEL_URL")



# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'debug.log'),
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }





