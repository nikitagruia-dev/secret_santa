from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
from drf_util.config import default_logging, load_environment

from .base import *

ALLOWED_HOSTS = ["*"]
WSGI_AUTO_RELOAD = True
DEBUG = True

load_dotenv(verbose=True)

ENV_VARS = {
    'SQL_ENGINE': {
        'required': True,
        'default': 'django.db.backends.postgresql_psycopg2',
    },
    'SQL_NAME': {
        'required': True,
    },
    'SQL_USER': {
        'required': True,
    },
    'SQL_PASSWORD': {
        'required': True,
    },
    'SQL_HOST': {
        'required': True,
    },
    'SQL_PORT': {
        'required': True,
    },
    'SECRET_KEY': {
        'required': True,
    },
    'EMAIL_USE_TLS': {
        'required': False,
        'default': False,
        'parse': lambda val: True if val == 'True' else False
    },
    'EMAIL_HOST': {},
    'EMAIL_HOST_USER': {},
    'EMAIL_HOST_PASSWORD': {},
    'EMAIL_PORT': {
        'parse': lambda val: int(val)
    },
    'RAVEN_CONFIG_DNS': {},
    'BASE_URL_PATH': {},
    'NOTIFICATION_SERVICE_URL': {},
    'DOMAIN_ADDRESS': {
        'required': True
    },
}

local_vars = load_environment(ENV_VARS, locals())
LOGGING = default_logging(local_vars.get('DEBUG_LEVEL'))

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': local_vars.get('SQL_ENGINE'),
        'NAME': local_vars.get('SQL_NAME'),
        'USER': local_vars.get('SQL_USER'),
        'PASSWORD': local_vars.get('SQL_PASSWORD'),
        'HOST': local_vars.get('SQL_HOST'),
        'PORT': local_vars.get('SQL_PORT'),
    }
}

EMAIL_USE_TLS = local_vars.get('EMAIL_USE_TLS')
EMAIL_HOST = local_vars.get('EMAIL_HOST')
EMAIL_HOST_USER = local_vars.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = local_vars.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = local_vars.get('EMAIL_PORT')

RAVEN_CONFIG = {
    'dsn': local_vars.get('RAVEN_CONFIG_DNS'),
}

BASE_URL_PATH = local_vars.get('BASE_URL_PATH')
