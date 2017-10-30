# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os

from derpconf.config import Config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if 'test' in sys.argv:
    config_file = os.path.join(BASE_DIR, 'politicos', 'tests.config')
else:
    config_file = os.path.join(BASE_DIR, 'politicos', 'local.config')

if os.path.isfile(config_file):
    conf = Config.load(config_file)
else:
    conf = Config()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = conf.get('SECRET_KEY', 'REPLACE-THIS-IN-CONFIG-LOCAL')

DEBUG = conf.get('DEBUG', True)

ALLOWED_HOSTS = conf.get('ALLOWED_HOSTS', [])

DEFAULT_INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'bootstrap3',
    'django_markup',
    'politicians',
    'website',
    'captcha',
    'tastypie',
    'tastypie_swagger',
    'cacheops',
    'django_extensions',
    'raven.contrib.django.raven_compat',
)
INSTALLED_APPS = conf.get('INSTALLED_APPS', DEFAULT_INSTALLED_APPS)

TASTYPIE_DEFAULT_FORMATS = conf.get('TASTYPIE_DEFAULT_FORMATS', ['json'])

CORS_ORIGIN_ALLOW_ALL = conf.get('CORS_ORIGIN_ALLOW_ALL', True)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'politicos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'website', 'templates', 'tastypie_swagger'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'politicos.wsgi.application'

DEAFAULT_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DATABASES = conf.get('DATABASES', DEAFAULT_DATABASE)

SITE_ID = conf.get('SITE_ID', 1)

LANGUAGE_CODE = conf.get('LANGUAGE_CODE', 'pt-br')

TIME_ZONE = conf.get('TIME_ZONE', 'UTC')

USE_I18N = conf.get('USE_I18N', True)

USE_L10N = conf.get('USE_L10N', True)

USE_TZ = conf.get('USE_TZ', True)

MEDIA_URL = conf.get('MEDIA_URL', '/media/')
MEDIA_ROOT = conf.get('MEDIA_ROOT', '')

STATIC_URL = conf.get('STATIC_URL', '/static/')
STATIC_ROOT = conf.get('STATIC_ROOT', '')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_URL = conf.get('LOGIN_URL', '/admin/')

RESOURCE_CACHE_TIMEOUT = conf.get('RESOURCE_CACHE_TIMEOUT', 60)

RESOURCE_MAX_REQUESTS = conf.get('RESOURCE_MAX_REQUESTS', 500)

DEAFAULT_CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 60
    },
}
CACHES = conf.get('CACHES', DEAFAULT_CACHES)

TSE_CONCURRENCY = conf.get('TSE_CONCURRENCY', 2)

LOG_DIR = conf.get('LOG_DIR', '/tmp')

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',  # noqa
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
        'politicos_command_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/error.log',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'politicos_command': {
            'handlers': ['console', 'politicos_command_error'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}
LOGGING = conf.get('LOGGING', DEFAULT_LOGGING)

DEFAULT_CACHEOPS_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 1,
    'socket_timeout': 3,
}
CACHEOPS_REDIS = conf.get('CACHEOPS_REDIS', DEFAULT_CACHEOPS_REDIS)

DEFAULT_CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60
}
CACHEOPS_DEFAULTS = conf.get('CACHEOPS_DEFAULTS', DEFAULT_CACHEOPS_DEFAULTS)

DEFAULT_CACHEOPS = {
    'auth.user': {'ops': 'get', 'timeout': 60 * 15},
    'auth.*': {'ops': ('fetch', 'get')},
    'auth.permission': {'ops': 'all'},
    'politicians.*': {'ops': 'all'},
    '*.*': {},
}
CACHEOPS = conf.get('CACHEOPS', DEFAULT_CACHEOPS)

CACHEOPS_DEGRADE_ON_FAILURE = True

RECAPTCHA_PUBLIC_KEY = conf.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = conf.get('RECAPTCHA_PRIVATE_KEY')

CONTACT_US_EMAIL = conf.get('CONTACT_US_EMAIL', '')

RAVEN_CONFIG = conf.get('RAVEN_CONFIG', {'dsn': ''})
