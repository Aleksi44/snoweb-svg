from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from decouple import config

DEBUG = False

ADMINS = [('Snoweb', 'hello@snoweb.fr')]

SECRET_KEY = config('SECRET_KEY', default='debug')

ALLOWED_HOSTS = [config('ALLOWED_HOSTS', default='0.0.0.0')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME', default='postgres'),
        'USER': config('DATABASE_USER', default='postgres'),
        'PASSWORD': config('DATABASE_PASSWORD', default='postgres'),
        'HOST': 'snowebsvg_db',
        'PORT': '5432',
    }
}

ANYMAIL = {
    "SENDGRID_API_KEY": config('SENDGRID_API_KEY', default='debug'),
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "hello@snoweb.io"
SERVER_EMAIL = "hello@snoweb.io"

SENTRY_DNS = config('SENTRY_DNS', default=None)
if SENTRY_DNS:
    sentry_sdk.init(
        dsn=SENTRY_DNS,
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

DJANGO_CSS_INLINE_ENABLE = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'snowebsvg_memcached:11211',
    }
}

CSRF_COOKIE_SECURE = True

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default=None)
if AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID:
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_DISTRIBUTION_ID = config('AWS_DISTRIBUTION_ID')
    AWS_IS_GZIPPED = True
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = False
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'public, max-age=31536000',
    }
    STATIC_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
    MEDIA_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
