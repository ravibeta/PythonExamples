"""
Django settings for metricapi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os

try:
    from ConfigParser import RawConfigParser
except:
    from configparser import RawConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

parser = RawConfigParser()
parser.read(BASE_DIR + '/config.ini')


SECRET_KEY = '19--ge%i6m@ax#=d1-!e*dmm=&=t@!qs%u!))_+k22(lgdy4zw'

DEBUG = False

TEMPLATE_DEBUG = parser.get('global','debug')

ALLOWED_HOSTS = ['*']


app_list = [
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
]

middleware_list = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
app_list.append('api')
app_list.append('api.v1')

ENVIRONMENT = parser.get('global','environment')
app_list.append('django.contrib.auth')
app_list.append('django.contrib.contenttypes')
middleware_list.append('django.contrib.auth.middleware.AuthenticationMiddleware')
middleware_list.append('django.contrib.auth.middleware.SessionAuthenticationMiddleware')


INSTALLED_APPS = tuple(app_list)

MIDDLEWARE_CLASSES = tuple(middleware_list)



ROOT_URLCONF = 'metricapi.urls'

WSGI_APPLICATION = 'metricapi.wsgi.application'


# Application configuration settings
#ENVIRONMENT = parser.get('global','environment')



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },        
        'request_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': parser.get('global', 'log_path')+'request.log',
        },
        'app_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': parser.get('global', 'log_path')+'request.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['request_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api': {
            'handlers': ['app_log'],
            'level': 'INFO',
            'propagate': True,
        }
    },    
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = 'smtpserver.myinc.com'


STATIC_URL = '/static/'
STATIC_ROOT = parser.get('global', 'static_path')
ALLOWED_STATIC_PATH = ['documentation', 'documentationapi-docs', 'static']

SWAGGER_SETTINGS = {
    'exclude_namespaces': ["test_api_call"],
    'api_version': '1.0',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': False,
    'is_superuser': False,
    'permission_denied_handler': None,
    'doc_expansion': 'none',
}
