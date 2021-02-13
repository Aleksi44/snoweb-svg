import os
import environ

BASE_DIR = os.environ['BASE_DIR']
env = environ.Env()
environ.Env.read_env(BASE_DIR + '/.env')

DEBUG = env.bool('DEBUG', default=True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
SECRET_KEY = env.str('SECRET_KEY', default='debug_key')

ALLOWED_HOSTS = [
                    '127.0.0.1',
                    'localhost',
                ] + env.list('DOMAINS', default=[])

INSTALLED_APPS = [
    'snowebsvg',
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "django.contrib.sitemaps",
    'storages',
    'django_css_inline'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'app.middlewares.SettingsMiddleware',
]


def constants_processor(request):
    from snowebsvg import settings
    return {
        'settings': settings,
        'debug': DEBUG,
        'LANGUAGE_CODE': LANGUAGE_CODE
    }


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'snowebsvg/templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.settings.constants_processor'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'libraries': {
                'debug': 'app.templatetags.debug',
            }
        },
    },
]

SITE_ID = 1
ROOT_URLCONF = 'urls'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# AWS


AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY', None)
AWS_S3_REGION_NAME = env.str('AWS_S3_REGION_NAME', None)
AWS_S3_CUSTOM_DOMAIN = env.str('AWS_S3_CUSTOM_DOMAIN', None)
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME', None)
AWS_DISTRIBUTION_ID = env.str('AWS_DISTRIBUTION_ID', None)

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    AWS_IS_GZIPPED = True
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = False
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'public, max-age=31536000',
    }
    STATIC_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# LOGGING


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'app.formatter.DjangoColorsFormatter',
            'format': '[%(asctime)s] %(levelname)s\033[0m \033[1m%(name)s\033[0m -> %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'snowebsvg': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

# INTERNATIONALIZATION

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', "English"),
    ('fr', "French"),
]

DJANGO_CSS_INLINE_ENABLE = not DEBUG
