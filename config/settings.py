# """
# Django settings for config project.
# """

# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # Quick-start development settings - unsuitable for production
# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-!k7px@!_u9y6g*-x2506gd%q1vc$1u@$+ph!tma^)bj9@nm14-'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# # 1. FIX for DisallowedHost Error (HTTP_HOST header)
# ALLOWED_HOSTS = [
#     'ecommerce-website-mg4g.onrender.com',  # Your live Render URL
#     '127.0.0.1',                            # Local development
#     'localhost',                            # Local development
# ]

# # 2. FIX for CSRF Verification Failed Error (Origin checking)
# # This is required because your site is running over HTTPS on Render.
# CSRF_TRUSTED_ORIGINS = [
#     'https://ecommerce-website-mg4g.onrender.com',
# ]


# # Application definition

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     'store.apps.StoreConfig',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'config.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 # THIS LINE MUST BE HERE FOR THE ADMIN TO WORK:
#                 'django.contrib.auth.context_processors.auth', 
#                 'django.contrib.messages.context_processors.messages',
#                 # Removed duplicate 'django.contrib.auth.context_processors.auth'
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'config.wsgi.application'


# # Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # Internationalization
# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# STATIC_URL = '/static/'

# # Media URL and Root
# MEDIA_URL = '/upload/'
# MEDIA_ROOT = BASE_DIR / 'upload'


# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# # --- Real SMTP Configuration (Using TLS on Port 587) ---
# # NOTE: It is a security risk to hardcode credentials like this in production.
# # They should be moved to environment variables (e.g., using python-decouple or os.environ).
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# # Use TLS (Transport Layer Security) on port 587
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587         
# EMAIL_USE_TLS = True     
# EMAIL_USE_SSL = False    

# # Your actual credentials (using regular password since 2FA is off)
# EMAIL_HOST_USER = 'harshadchavare210@gmail.com' # <-- UPDATED EMAIL USER
# EMAIL_HOST_PASSWORD = 'ciin xyzg lcif fxvj' 

# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
"""
Django settings for config project.
"""
import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: Get the Secret Key from the environment, or use a dummy one locally
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-key-change-in-prod')

# SECURITY: Default to True locally, but strictly False on Render
DEBUG = 'RENDER' not in os.environ

# HOSTS: Allow Render URL and localhost
ALLOWED_HOSTS = [
    'ecommerce-website-mg4g.onrender.com',  # Your live Render URL
    '127.0.0.1',                            # Local development
    'localhost',                            # Local development
]
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])

# Trusted Origins for HTTPS
# if RENDER_EXTERNAL_HOSTNAME:
#     CSRF_TRUSTED_ORIGINS ='ecommerce-website-mg4g.onrender.com'
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS = ['https://ecommerce-website-mg4g.onrender.com'] 

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- DATABASE CONFIGURATION ---
# Locally: Uses SQLite
# On Render: Uses PostgreSQL (Neon) via DATABASE_URL variable
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require='RENDER' in os.environ, # Force SSL on Render
    )
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC FILES (CSS/JS) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise Configuration for best performance and compression
if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

# --- EMAIL CONFIGURATION ---
# Credentials are now pulled from Environment Variables for safety
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')     # Set this in Render Dashboard
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS') # Set this in Render Dashboard
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'