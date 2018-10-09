"""Django settings for HEMARatings.submit project."""

import os
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backend')

DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
TEMPLATE_DEBUG = DEBUG
CORS_ORIGIN_ALLOW_ALL = DEBUG

SECRET_KEY = 'I\'M NOT SECRET UNLESS YOU CHANGE ME'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
    'corsheaders',

    'submit',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
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


PAGE_CACHE_SECONDS = 60

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        # 'NAME': os.environ['DB_NAME'],
        # 'USER': os.environ['DB_USER'],
        # 'PASSWORD': os.environ['DB_PASS'],
        # 'HOST': os.environ['DB_HOST'],
        # 'PORT': os.environ['DB_PORT'],
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        }
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format':
            '%(levelname)s %(asctime)s %(module)s '
            '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ['REDIS_URI']}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_TIMEOUT": 900,
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

DEFAULT_LOGGER = 'raven'

LOGGER_EXCEPTION = DEFAULT_LOGGER
LOGGER_ERROR = DEFAULT_LOGGER
LOGGER_WARNING = DEFAULT_LOGGER
