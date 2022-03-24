from .base import *

from decouple import config
import json

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'debug_key'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME', default='snowebsvg'),
        'USER': config('DATABASE_USER', default='snowebsvg'),
        'PASSWORD': config('DATABASE_PASSWORD', default='postgres'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DJANGO_CSS_INLINE_ENABLE = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
