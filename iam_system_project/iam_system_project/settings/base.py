# iam_system_project/settings/base.py
from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  
]

THIRD_PARTY_APPS = [
    'django_password_validators',
]

LOCAL_APPS = [
    'models', # This app is designed to store the models.
    'authentication',
    'task_management',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_PASSWORD_VALIDATORS = [
   
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    }, 
    
    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
        'OPTIONS': {
             'min_length_digit': 1,
             'min_length_alpha': 0,
             'min_length_special': 1,
             'min_length_lower': 1,
             'min_length_upper': 1,
             'special_characters': "~!@#$%^&*()_+{}\":;'[]"
         }
    },
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

ROOT_URLCONF = 'iam_system_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # Add your project-specific templates directory
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

AUTH_USER_MODEL = "models.CustomUser"

ACCOUNT_ACTIVATION_DAYS = 7  # Number of days to wait for account activation

WSGI_APPLICATION = 'iam_system_project.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
