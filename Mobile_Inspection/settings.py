"""
Django settings for Mobile_Inspection project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path
import os
import datetime
from datetime import timedelta
import smtplib

# import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9=tl3ssl58r1ah-ninw4=z@!y-u92wte^cs=yn)=708_q^^tn='

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
    'Mobile_Inspectionapp',
    'payment_app',
    'corsheaders',
    'rest_framework',
    'phonenumber_field',
    'phonenumbers',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
]

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

ROOT_URLCONF = 'Mobile_Inspection.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'Mobile_Inspection.wsgi.application'


# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',

],
    'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.IsAuthenticated',
       'rest_framework.permissions.IsAdminUser',

       ]
}

REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': (
          'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}



DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql', 
    'NAME': 'Mobile_Inspection_Management',
    'USER': 'root',
    'PASSWORD': '',#Admin@123
    'HOST': 'localhost', # Or an IP Address that your DB is hosted on
    'PORT': '3306',
    'OPTIONS': {
            'read_default_file': '/opt/lampp/etc/my.cnf',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://intuitiveagilesolution.com:8000",
    "http://54.201.14.154:8000",
    "http://54.201.14.154",
    "http://3.90.226.115",
    "https://inspectionsquad.com"
    ]

STATICFILES_DIRS = [
    BASE_DIR,"static"
]
MEDIA_ROOT = BASE_DIR /"static/media"
MEDIA_URL = "/media/"
BASE_URL="http://127.0.0.1:8000"

AUTH_USER_MODEL = 'Mobile_Inspectionapp.user'


# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',

}


#Stripe
API_PUBLISH_KEY = 'pk_test_51LixZiJTvBqbiOKnPcS69thhnqhwWqXz4RZteSKyoBjG1CytGinFMveOjGlNUqE7F9AZYpJRasUy1uwhxSrpZvoO008CcnCRNR'
API_SECRET_KEY = 'sk_test_51LixZiJTvBqbiOKnTOF6W6uR1T0f8DMSg6vcAIgyUbTsglCBVOtFy3EK0RlNOVet8OIaXczjMx24otCXwbBd2Msm00PQNhYgJr'

#Paypal
CLIENT_ID = "AZbSbes1HlwmiI-7wGONJKIA8XTptRIxkKrZ1HSha7mVStBhTr98OVifJxEe2dYjOtxNo3laHlMFzeg1"
CLIENT_SECRET = "EM4WGzdZpnTMm1ynRm29D_rSUEOpbgj3d5JWVLg-LAtpEUnrPQNe1ClXbeznBqmQC6k3F6mRkhLKMsh8"

#Email Configration
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 #465#
EMAIL_HOST_USER = "email host user"
EMAIL_HOST_PASSWORD = "password"
EMAIL_USE_TLS = True
PASSWORD_RESET_TIMEOUT= 900 #sec=15 minutes, 
