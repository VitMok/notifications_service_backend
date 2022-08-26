"""
Django settings for notification_service_backend project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv("DEBUG", "0")))

ALLOWED_HOSTS = []


# ___   ___  ___  ____
# / _ | / _ \/ _ \/ __/
# / __ |/ ___/ ___/\ \`
# /_/ |_/_/  /_/  /___/

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'django.contrib.postgres',
    'drf_spectacular',

    'apps.notifications',
]

# __  __________  ___  __   _____      _____   ___  ____
# /  |/  /  _/ _ \/ _ \/ /  / __/ | /| / / _ | / _ \/ __/
# / /|_/ // // // / // / /__/ _/ | |/ |/ / __ |/ , _/ _/
# /_/  /_/___/____/____/____/___/ |__/|__/_/ |_/_/|_/___/

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'notification_service_backend.urls'

# ____________  ______  __   ___ ______________
# /_  __/ __/  |/  / _ \/ /  / _ /_  __/ __/ __/
# / / / _// /|_/ / ___/ /__/ __ |/ / / _/_\ \
# /_/ /___/_/  /_/_/  /____/_/ |_/_/ /___/___/

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

WSGI_APPLICATION = 'notification_service_backend.wsgi.application'


# ___  ___
# / _ \/ _ )
# / // / _  |
# /____/____/

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}


#   ___  ___   ________  _   _____   __   _______  ___ ______________  _  __
#  / _ \/ _ | / __/ __/ | | / / _ | / /  /  _/ _ \/ _ /_  __/  _/ __ \/ |/ /
# / ___/ __ |_\ \_\ \   | |/ / __ |/ /___/ // // / __ |/ / _/ // /_/ /    /
# /_/  /_/ |_/___/___/   |___/_/ |_/____/___/____/_/ |_/_/ /___/\____/_/|_/

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


# __   ____  ________   __   ____
# / /  / __ \/ ___/ _ | / /  / __/
# / /__/ /_/ / /__/ __ |/ /__/ _/
# /____/\____/\___/_/ |_/____/___/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIME_ZONE', 'Europe/Moscow')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# ___  ______________
# / _ \/ __/ __/_  __/
# / , _/ _/_\ \  / /
# /_/|_/___/___/ /_/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ______  ______   ______
# / __/  |/  / _ | /  _/ /
# / _// /|_/ / __ |_/ // /__
# /___/_/  /_/_/ |_/___/____/

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')

EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')

# REDIS
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

# ___________   _________  __
# / ___/ __/ /  / __/ _ \ \/ /
# / /__/ _// /__/ _// , _/\  /
# \___/___/____/___/_/|_| /_/

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = 'Europe/Moscow'

JWT_TOKEN = os.getenv('JWT_TOKEN')