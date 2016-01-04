"""
Django settings for leaseapi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

try:
    from ConfigParser import RawConfigParser
except:
    from configparser import RawConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

parser = RawConfigParser()
parser.read(BASE_DIR + '/config.ini')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '19--ge%i6m@ax#=d1-!e*dmm=&=t@!qs%u!))_+k22(lgdy4zw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = parser.get('global','debug')

ALLOWED_HOSTS = ['.adobe.com']

#TEST_RUNNER = 'api.tests.ByPassCifsTestRunner.ByPassCifsTestRunner'
#JENKINS_TEST_RUNNER = 'api.tests.ByPassCifsTestRunner.ByPassCifsTestRunner'

# tell django where to put the auth migrations
#MIGRATION_MODULES = {
   # key: app name, value: a fully qualified package name, not the usual `app_label.something_else`
#  'auth': 'django.contrib.auth',
#}

app_list = [
    'django_jenkins',
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
if 'test' not in ENVIRONMENT:
    AUTHENTICATION_BACKENDS = ('cloudapi_utils.backend.AdobeBackend', )
    app_list.append('cloudapi_utils')
    middleware_list.append('cloudapi_utils.middleware.AdobeOauth2Middleware')
    TEMPLATE_DEBUG = False
else:
    app_list.append('cloudapi_utils')
    app_list.append('django.contrib.auth')
    app_list.append('django.contrib.contenttypes')
    middleware_list.append('django.contrib.auth.middleware.AuthenticationMiddleware')
    middleware_list.append('django.contrib.auth.middleware.SessionAuthenticationMiddleware')


INSTALLED_APPS = tuple(app_list)

MIDDLEWARE_CLASSES = tuple(middleware_list)


# Application definition
"""
INSTALLED_APPS = (
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.messages',
    'django_jenkins',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'cloudapi_utils',
)


PROJECT_APPS = (
    'api',
)
"""
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_flake8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
)

#INSTALLED_APPS += PROJECT_APPS
"""
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cloudapi_utils.middleware.AdobeOauth2Middleware',
)

AUTHENTICATION_BACKENDS = ('cloudapi_utils.backend.AdobeBackend', )
"""
ROOT_URLCONF = 'leaseapi.urls'

WSGI_APPLICATION = 'leaseapi.wsgi.application'


# Application configuration settings
#ENVIRONMENT = parser.get('global','environment')
CIFS_BACKUP_EMAIL = parser.get('mail','backup_mail')
ITC_DEV_MAIL = parser.get('mail','dev_mail')
ADMIN_EMAIL = parser.get('mail','admin_mail')
EMAIL_SUBJECT = parser.get('mail','global_subject')
TEST_EMAIL = parser.get('mail','test_mail')
SERVICE_NAME = parser.get('global','service') 
CIFS_USER = parser.get('global','cifs_user') 
SSH_KEY_PATH = parser.get('global', 'ssh_key_path')
GRPMGR_API_KEY = parser.get('groupmanager', 'apikey')
VCO_EMAIL = parser.get('vco', 'vco_email')
VCO_PASSWORD = parser.get('vco', 'vco_password')

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if 'jenkins' in os.sys.argv or 'test' in os.sys.argv:
    DATABASES = {
        'default': {
             'ENGINE': 'django.db.backends.mysql',
             'HOST': parser.get('database','db_test_host'),   # Or an IP Address that your DB is hosted on
             'PORT': parser.get('database','db_test_port'),
             'NAME': parser.get('database','db_test_name'),
             'USER': parser.get('database','db_test_user'),
             'PASSWORD': parser.get('database','db_test_password'),
         }
    }
else:
    DATABASES = {
        'default': {
             'ENGINE': 'django.db.backends.mysql',
             'HOST': parser.get('database','db_host'),   # Or an IP Address that your DB is hosted on
             'PORT': parser.get('database','db_port'),
             'NAME': parser.get('database','db_name'),
             'USER': parser.get('database','db_user'),
             'PASSWORD': parser.get('database','db_password'),
         }
    }

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': parser.get('database','db_host'),   # Or an IP Address that your DB is hosted on
        'PORT': parser.get('database','db_port'),
        'NAME': parser.get('database','db_name'),
        'USER': parser.get('database','db_user'),
        'PASSWORD': parser.get('database','db_password'),
        'TEST_HOST': parser.get('database','db_test_host'),   # Or an IP Address that your DB is hosted on
        'TEST_PORT': parser.get('database','db_test_port'),
        'TEST_NAME': parser.get('database', 'db_test_name'),
        'TEST_USER': parser.get('database','db_test_user'),
        'TEST_PASSWD': parser.get('database','db_test_password'),
    }
}
'''

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
            'class':'django.utils.log.NullHandler',
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

#REST_FRAMEWORK = {
#    'DEFAULT_PARSER_CLASSES': (
#        'rest_framework.parsers.JSONParser',
#    ),
#    'DEFAULT_PAGINATION_CLASS': 'cloudapi_utils.pagination.AdobePagination',
#    'PAGINATE_BY': 10,
#    'EXCEPTION_HANDLER': 'cloudapi_utils.exceptions.custom_exception_handler'
#}


#JENKINS_TASKS = ( 
#    'django_jenkins.tasks.run_pep8', 
#    'django_jenkins.tasks.run_pylint', 

#)
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = 'europemail.eur.adobe.com'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

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
