"""
Django settings for ch_bot project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^_uk7qe5*p^=@1#fchzi(jy7dk%(*ciuzwyp$gfmn@@v&1wb2r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# Telegram token and  domain name

TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')
MY_DOMAIN = os.getenv('DOMAIN_NAME')

# Application definition

INSTALLED_APPS = [
    'payments.apps.PaymentsConfig',
    't_bot.apps.TBotConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ch_bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

WSGI_APPLICATION = 'ch_bot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
# Variables of payment systems

# OBMENKA

CARD_NUMBER = os.getenv("CARD_NUMBER", "error_card_number")
OPERATOR_ID = os.getenv("OPERATOR_ID", "error operator")
ACQUIRING_URL = "https://acquiring_api.obmenka.ua"
ACQUIRING_SALT = os.getenv("SALT", "error_salt")
ACQUIRING_TEST_SALT = os.getenv("TEST_SALT", "error_salt")
ACQUIRING_CLIENT_NUM = os.getenv("CLIENT_ID", "error_num")

# WESTWALLET

WESTWALLET_PUBLIC_KEY = os.getenv("WESTWALLET_PUBLIC", "error_key")
WESTWALLET_PRIVATE_KEY = os.getenv("WESTWALLET_PRIVATE", "error_key")

# 3 system

IP_WHITELIST_AD = os.getenv("IP_WHITELIST_AD", "error_list").split(';')
AD_WEBHOOK_SECRET = os.getenv("AD_WEBHOOK_SECRET", "error_secret")
AD_CLIENT_ID = os.getenv("AD_CLIENT_ID", "error_id")
AD_CLIENT_SECRET = os.getenv("AD_CLIENT_SECRET", "error_secret")
AD_API_URL = "https://api.adgroup.finance/bill-payment/invoice/create"