"""
Django settings for config project.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!k7px@!_u9y6g*-x2506gd%q1vc$1u@$+ph!tma^)bj9@nm14-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 1. FIX for DisallowedHost Error (HTTP_HOST header)
ALLOWED_HOSTS = [
    'ecommerce-website-mg4g.onrender.com',  # Your live Render URL
    '127.0.0.1',                            # Local development
    'localhost',                            # Local development
]

# 2. FIX for CSRF Verification Failed Error (Origin checking)
# This is required because your site is running over HTTPS on Render.
CSRF_TRUSTED_ORIGINS = [
    'https://ecommerce-website-mg4g.onrender.com',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'store.apps.StoreConfig',
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

ROOT_URLCONF = 'config.urls'

# config/settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                # THIS LINE MUST BE HERE FOR THE ADMIN TO WORK:
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Media URL and Root
MEDIA_URL = '/upload/'
MEDIA_ROOT = BASE_DIR / 'upload'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Real SMTP Configuration (Using TLS on Port 587) ---
# NOTE: It is a security risk to hardcode credentials like this in production.
# They should be moved to environment variables (e.g., using python-decouple or os.environ).
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Use TLS (Transport Layer Security) on port 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587         # Changed from 465
EMAIL_USE_TLS = True     # Changed from False
EMAIL_USE_SSL = False    # Changed from True

# Your actual credentials (using regular password since 2FA is off)
EMAIL_HOST_USER = 'harshadchavare210@gmail.com'
EMAIL_HOST_PASSWORD = 'Harshad123456' # <-- Updated to your regular password

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER