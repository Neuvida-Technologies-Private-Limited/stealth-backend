import os
from datetime import timedelta


# CONFIG_DIR points to config package (project/src/apps/config)
CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# BASE_DIR points to starting point of the projects's base directory path (<project_name>/(config, apps))
BASE_DIR = os.path.abspath(os.path.join(CONFIG_DIR, '..'))

# ASSETS_MEDIA_DIR points to the top level directory (one directory up from BASE_DIR)
# assets, media, database, and venv will be located in this directory
ASSETS_MEDIA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

# APPS_DIR points to the core package (project/src/apps).
# All custom apps and newly created apps will be located in this directory.
APPS_DIR = os.path.join(BASE_DIR, 'apps')

BUILT_IN_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'debug_toolbar',
    'tagging'
]
USER_DEFINED_APPS = [
    'apps.core',
    'apps.access',
    'apps.keymanagement',
    'apps.library',
    'apps.prompt',
    'apps.workspace',
]
INSTALLED_APPS = BUILT_IN_APPS + THIRD_PARTY_APPS + USER_DEFINED_APPS


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'YOUR_GOOGLE_CLIENT_ID',
            'secret': 'YOUR_GOOGLE_CLIENT_SECRET',
            'key': '',
        }
    }
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),  # Access token lifetime (2 hours)
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # Token refresh lifetime (1 day)
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=2),  # Sliding token lifetime (2 hours)
    'SLIDING_TOKEN_REFRESH_LIFETIME_GRACE_PERIOD': timedelta(minutes=15),  # Grace period for token refresh (15 minutes)
    'ROTATE_REFRESH_TOKENS': False,  # Rotate refresh tokens (False by default)
    'ALGORITHM': 'HS256',  # Token signing algorithm
    'SIGNING_KEY': "this is my secret key",  # Secret key for token signing
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S.%fZ",
    "UNICODE_JSON": False,
    "DEFAULT_RENDERER_CLASS": ("rest_framework.renderers.JSONRenderer",),
}

BUILT_IN_MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
THIRD_PARTY_MIDDLEWARE = []
USER_DEFINED_MIDDLEWARE = []
MIDDLEWARE = BUILT_IN_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE + USER_DEFINED_MIDDLEWARE

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Password validation
# https://docs.djangonew.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangonew.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files')  # project/core/static_files
]
STATIC_ROOT = os.path.join(ASSETS_MEDIA_DIR, 'assets')  # project/assets

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ASSETS_MEDIA_DIR, 'media')  # project/media
