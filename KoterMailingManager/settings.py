"""
Django settings for KoterMailingManager project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import re

import environ, os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    KOTER_DEBUG=(bool, False),
    KOTER_DATABASE=(str, "sqlite:///koter.db"),
    KOTER_ALLOWED_HOSTS=(list, []),
    KOTER_TIME_ZONE=(str, "UTC"),
    KOTER_ID_LENGTH=(int, 18),
    KOTER_PHONE_NUMBER_REGION=(str, "BR"),
    KOTER_CORS_ALLOWED_ORIGINS=(list, []),
    GOOGLE_API_KEY=(str, "AIzaSyD--your-google-maps-key-SjQBE")
)

environ.Env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("KOTER_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("KOTER_DEBUG")

ALLOWED_HOSTS = env.list("KOTER_ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    "daphne",
    'discord_integration',
    "KTApp",
    'baton',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'config_models',
    'phonenumber_field',
    'import_export',
    "taggit",
    'auditlog',
    "address",
    'django_extensions',
    "corsheaders",
    'rest_framework',
    "rest_framework_datatables",
    "rest_framework_api_key",
    "log_viewer",
    'watchman',
    'KTLogger',
    "ajax_datatable",
    'baton.autodiscover',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'requestlogs.middleware.RequestLogsMiddleware',
    'requestlogs.middleware.RequestIdMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'KoterMailingManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'KoterMailingManager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': env.db("KOTER_DATABASE")
}

CACHES = {
    'default': env.cache("KOTER_CACHE"),
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env.str("KOTER_TIME_ZONE")

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BATON = {
    'SITE_HEADER': 'Koter Mailing Manager',
    'SITE_TITLE': 'Koter Mailing Manager',
    'INDEX_TITLE': 'Administration',
    'SUPPORT_HREF': 'https://github.com/otto-torino/django-baton/issues',
    'COPYRIGHT': 'copyright ?? 2022 <a href="https://www.4u360.com.br">4U360</a>',
    'POWERED_BY': '<a href="https://github.com/riquedev">Henrique da Silva Santos</a>',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'CHANGELIST_FILTERS_IN_MODAL': True,
    'CHANGELIST_FILTERS_ALWAYS_OPEN': False,
    'CHANGELIST_FILTERS_FORM': True,
    'MENU_ALWAYS_COLLAPSED': False,
    'MENU_TITLE': 'Menu',
    'MESSAGES_TOASTS': False,
    'GRAVATAR_DEFAULT_IMG': 'mp',
    'LOGIN_SPLASH': '/static/ktapp/img/656670.webp',
    'SEARCH_FIELD': {
        'label': _('Search contents...'),
        'url': reverse_lazy('KT:admin_search'),
    },
    'MENU': (
        {'type': 'title', 'label': 'main', 'apps': ('auth', 'ktapp')},
        {
            'type': 'app',
            'name': 'auth',
            'label': 'Authentication',
            'icon': 'fa fa-lock',
            'models': (
                {
                    'name': 'user',
                    'label': 'Users'
                },
                {
                    'name': 'group',
                    'label': 'Groups'
                },
            )
        },

        {'type': 'free', 'label': _("Audit"), 'default_open': True, 'children': [
            {'type': 'free', 'label': _("Requests"), 'url': reverse_lazy("KTLogger:file", args=[
                "logs/" + env.str("KOTER_REQUEST_LOG_FILE", "koter-requests.log")
            ])},
        ]},
        {'type': 'model', 'icon': 'fa fa-cog', 'label': 'Configurations', 'name': 'koterconfiguration', 'app': 'ktapp'},
        {'type': 'free', 'icon': 'fas fa-sign-out-alt', 'label': _("Logout"), 'url': reverse_lazy('admin:logout')},
    ),
}

# Addons
ALLOW_ROBOTS = False
ADMINS = "4U360 <contato@4u360.com.br>"
MANAGERS = "No-Reply <no-reply@koter.com.br>"
SERVER_EMAIL = "contato@4u360.com.br"

SITE_ID = 1

# Koter setup
KOTER_ID_LENGTH = env.int("KOTER_ID_LENGTH")
PHONE_NUMBER_REGION = env.str("KOTER_PHONE_NUMBER_REGION")
KOTER_VERSION = "1.0.5-snapshot"
LOGIN_REDIRECT_URL = reverse_lazy("admin:index")
KOTER_EXTERNAL_USER_ID = "X-Koter-Id"
KOTER_INTEGRATION_ID = "X-Koter-Integration-Id"

CORS_ALLOWED_ORIGINS = env.list("KOTER_CORS_ALLOWED_ORIGINS", [])
# Rest framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "KTApp.permissions.APIIsEnabled",
        "rest_framework.permissions.IsAuthenticated",
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,
    'EXCEPTION_HANDLER': 'requestlogs.views.exception_handler',
}

# Google
GOOGLE_API_KEY = env.str("GOOGLE_API_KEY")

# Watchman
EXPOSE_WATCHMAN_VERSION = True
WATCHMAN_EMAIL_SENDER = env.str("WATCHMAN_EMAIL_SENDER", "")
WATCHMAN_EMAIL_RECIPIENTS = env.str("WATCHMAN_EMAIL_RECIPIENTS", "")

# Requestlog
REQUESTLOGS = {
    'SERIALIZER_CLASS': 'requestlogs.storages.RequestIdEntrySerializer',
    'REQUEST_ID_HTTP_HEADER': 'X_REQUEST_ID',
    'REQUEST_ID_ATTRIBUTE_NAME': 'request_id',
    'IGNORE_PATHS': [
        re.compile(r"/admin/"),
        re.compile(r"/baton/"),
        re.compile(r"/kt/"),
        re.compile(r"/static/"),
        re.compile(r"/media/"),
    ],
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'requestlogs_to_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': f'logs/{env.str("KOTER_REQUEST_LOG_FILE", "koter-requests.log")}',
            'formatter': 'request-formatter'
        },
        'discord_integration': {
            'level': 'DEBUG',
            'class': 'discord_integration.log.DiscordMessageHandler',
            'model_name': 'default',  # OPTIONAL: specify a name to use a different integration configuration.
        },
    },
    'loggers': {
        'requestlogs': {
            'handlers': ['requestlogs_to_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'root': {
            'handlers': ['discord_integration'],
            'level': 'DEBUG',
            'propagate': False
        }
    },
    'filters': {
        'request_id_context': {
            '()': 'requestlogs.logging.RequestIdContext',
        },
    },
    'formatters': {
        'request-formatter': {
            'format': '[%(levelname)s] %(asctime)s - %(message)s'
        },
    },
}

LOG_VIEWER_FILES = [
    # env.str("KOTER_REQUEST_LOG_FILE", "koter-requests.log")
]
LOG_VIEWER_FILES_PATTERN = '*.log*'
LOG_VIEWER_FILES_DIR = 'logs/'
LOG_VIEWER_PAGE_LENGTH = 25  # total log lines per-page
LOG_VIEWER_MAX_READ_LINES = 1000  # total log lines will be read
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25  # Max log files loaded in Datatable per page
LOG_VIEWER_PATTERNS = ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]']
LOG_VIEWER_EXCLUDE_TEXT_PATTERN = None  # String regex expression to exclude the log from line

# Optionally you can set the next variables in order to customize the admin:
# LOG_VIEWER_FILE_LIST_TITLE = "Custom title"
# LOG_VIEWER_FILE_LIST_STYLES = "/static/css/my-custom.css"


# ASGI
ASGI_APPLICATION = "KoterMailingManager.asgi.application"