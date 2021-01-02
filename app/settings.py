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
SECRET_KEY = '[V$xMycv[(YwhThQD+p[s@Wb@Ygy@:`M%D3I8Fs2tJ^Aw#ac$AJ65".*]uwPaK_'

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
    'app.middlewares.ThemeMiddleware',
]


def constants_processor(request):
    from snowebsvg import settings
    return {
        'settings': settings,
        'debug': DEBUG
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

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR
MEDIA_URL = '/'
