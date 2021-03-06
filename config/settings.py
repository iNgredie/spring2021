"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "'sk5rd932xh7k(qsqu@l!dwxg4px16vi7%&y+l$_*2n1=m0)&00'")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'drfpasswordless',
    'corsheaders',

    'src.users',
    'src.dynamic_settings',
    'src.tasks',
    'src.send_values',
    'src.services',
    'src.articles',

    'drf_spectacular'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGES = [
    ('ru', _('Russian')),
]

LANGUAGE_CODE = 'ru-RU'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static_back/'
STATIC_ROOT = BASE_DIR / 'static_back'

STATICFILES_DIRS = (
    BASE_DIR / 'static_be',
    '/media/items',
)

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'VERSION': '0.0.1',
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
    'TITLE': 'API ?????? ???????????????????? ???????????? ???????????? ????????????????????????????',
    'EXTERNAL_DOCS': {
        'url': 'https://docs.google.com/document/d/1u-DE_HC0Gx2DNU-sicepd36jyuZfp9UuEVZ5csqLNhQ/',
        'description': '???????????????? ??????????????'
    },
}

PASSWORDLESS_AUTH = {
    'PASSWORDLESS_AUTH_TYPES': ['EMAIL', 'MOBILE'],
    'PASSWORDLESS_EMAIL_NOREPLY_ADDRESS': 'asdadasasddasdsa@gmail.com',
    'PASSWORDLESS_AUTH_TOKEN_CREATOR': 'src.users.utils.get_token_for_user',
    'PASSWORDLESS_AUTH_TOKEN_SERIALIZER': 'src.users.serializers.JWTAuthTokenSerializer',
    'PASSWORDLESS_MOBILE_NOREPLY_NUMBER': 'Ssintensiv2',
    'PASSWORDLESS_MOBILE_MESSAGE': '?????? ?????? ?????????? ?? ????????????????????: %s',
    'PASSWORDLESS_SMS_CALLBACK': 'src.users.utils.smsc_send_sms_with_callback_token'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(
        minutes=int(os.environ.get('ACCESS_TOKEN_LIFETIME_IN_MINUTES', 1440))
    ),
}

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'SECRET')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'SECRET')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)

MY_SMSC_ACCOUNT = os.environ.get('MY_SMSC_ACCOUNT', 'SECRET')
MY_SMSC_PASSWORD = os.environ.get('MY_SMSC_PASSWORD', 'SECRET')


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://libera.pro",
    "https://housing.libera.pro",
    "http://management-company-chat-dev.spring-intensive-2021.simbirsoft1.com",
    "http://management-company-chat-test.spring-intensive-2021.simbirsoft1.com"
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://\w+\.dev\.brain4you\.ru$",
]

CORS_URLS_REGEX = r'^/api/v1/.*$'

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
