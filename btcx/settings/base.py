# Django settings for btcx (BTC Exchange) project.

import os
import sys
import djcelery
from datetime import timedelta
from django.utils import importlib

djcelery.setup_loader()

# Paths relative to base module path
PROJECT_PATH = os.path.join(os.path.dirname(__file__), '..')

# Environment from environment variable
ENV = os.environ.get('BTCX_ENV', 'dev')

# ----------------------------------------------------------------------------
# Base Django settings
# ----------------------------------------------------------------------------

DEBUG = True
TEMPLATE_DEBUG = DEBUG


WSGI_APPLICATION = 'btcx.wsgi.application'
ROOT_URLCONF = 'btcx.urls'
SECRET_KEY = 'xbr*6qhz(-e(&amp;6%8sh2e9lt(f=t(cx0_e8k8_jy+-_t)o3hh!-'

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

ADMINS = (
    ('Evan Culver', 'e@eculver.io'),
)

MANAGERS = ADMINS

# Admin media
ADMIN_MEDIA_ROOT = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static_build')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates').replace('\\', '/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'btcx.contrib.context_processors.default',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django_extensions',
    'btcx.apps.exchange',
    'djcelery',
)

# ----------------------------------------------------------------------------
# Services
# ----------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'btcx.db',
    }
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:1",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}

BROKER_URL = 'redis://localhost:6379/0'

CELERYBEAT_SCHEDULE = {
    'collect-mtgox': {
        'task': 'btcx.notifications.tasks.collect_mtgox',
        'schedule': timedelta(seconds=10),
    }
}

# ----------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': ''.join([
                '[%(asctime)s]',
                '[%(levelname)s] ',
                '%(name)s ',
                '%(filename)s:',
                '%(funcName)s:',
                '%(lineno)d | ',
                '%(message)s'
            ]),
            'datefmt': '%H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# ----------------------------------------------------------------------------
# Testing
# ----------------------------------------------------------------------------

# Use nose to run tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Detect test environment
TESTING = 'test' in sys.argv

if TESTING:
    # skip migrations and south tests when running tests
    SOUTH_TESTS_MIGRATE = False
    SKIP_SOUTH_TESTS = True

    # console logging for tests
    LOGGING['root']['handlers'] = ['console']


# ----------------------------------------------------------------------------
# App-specific settings
# ----------------------------------------------------------------------------

# commission to tack on to trade value
BTCX_COMMISSION = 0.01 #  1%
BTCX_KEYS = {
    'ASKS': 'XRT_CHECKPOINT',
    'BIDS': 'XRT_BTC_TO_USD',
}

# ----------------------------------------------------------------------------
# Enable extension via environment (warning: pretty hacky)
# ----------------------------------------------------------------------------

# try to import ``WEB_ENV``.py -- this is a little hacky, but it puts
# everything in wdapi.settings.``WEB_ENV``.py into ``locals()`` for this module
# TODO: is there a better way to do dynamic, relative '*' imports?
# TODO: pls fix me if possible
try:
    env_settings = importlib.import_module('..%s' % ENV, __name__)
    for s in dir(env_settings):
        locals()[s] = env_settings.__dict__[s]
except ImportError:
    pass  # we don't care if import fails


# ----------------------------------------------------------------------------
# DEBUG-specific last
# ----------------------------------------------------------------------------

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar', 'devserver')

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )

    DEVSERVER_MODULES = (
        'devserver.modules.sql.SQLRealTimeModule',
        'devserver.modules.sql.SQLSummaryModule',
        'devserver.modules.profile.ProfileSummaryModule',

        # Modules not enabled by default
        'devserver.modules.ajax.AjaxDumpModule',
        'devserver.modules.profile.MemoryUseModule',
        'devserver.modules.cache.CacheSummaryModule',
    )
