"""
Django settings for hypnos project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from kombu import Exchange, Queue
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bf82%m(v7l0r0@&5f01jxjc&^e%ttn3u_bglrcv6cy4=6)hu*l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ## by liam
    'hypnos',
    'celery_test',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hypnos.urls'

REST_FRAMEWORK = {  
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGINATE_BY': 10
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hypnos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hypnos',
        'USER': 'liam',
        'PASSWORD': 'liambao',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Redis comfiguration
REDIS = {
    'default': {
        'HOST': 'redis',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': ''
    }
}


RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')

if RABBIT_HOSTNAME.startswith('tcp://'):  
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

BROKER_URL = os.environ.get('BROKER_URL','')
if not BROKER_URL:  
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', 'liam'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'liambao'),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))

# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '?heartbeat=30'  
if not BROKER_URL.endswith(BROKER_HEARTBEAT):  
    BROKER_URL += BROKER_HEARTBEAT

BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10

# Celery configuration
# configure queues, currently we have only one
CELERY_DEFAULT_QUEUE = 'default'  
CELERY_QUEUES = (  
    Queue('default', Exchange('default'), routing_key='default'),
)

# Sensible settings for celery
CELERY_ALWAYS_EAGER = False  
CELERY_ACKS_LATE = True  
CELERY_TASK_PUBLISH_RETRY = True  
CELERY_DISABLE_RATE_LIMITS = False

# By default we will ignore result
# If you want to see results and try out tasks interactively, change it to False
# Or change this setting on tasks level
CELERY_IGNORE_RESULT = True  
CELERY_SEND_TASK_ERROR_EMAILS = False  
CELERY_TASK_RESULT_EXPIRES = 600

# Set redis as celery result backend
CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (
                        REDIS['default']['HOST'],
                        REDIS['default']['PORT'],
                        REDIS['default']['DB'])
CELERY_REDIS_MAX_CONNECTIONS = 1

# Don't use pickle as serializer, json is much safer
CELERY_TASK_SERIALIZER = "json"  
CELERY_ACCEPT_CONTENT = ['application/json']

CELERYD_HIJACK_ROOT_LOGGER = False  
CELERYD_PREFETCH_MULTIPLIER = 1  
CELERYD_MAX_TASKS_PER_CHILD = 1000  

# django-cacheops

# CACHEOPS_REDIS = "redis://%s%s:%d/%d" % (
#     (":" + REDIS['default']['PASSWORD'] + "@") if REDIS['default']['PASSWORD'] else '',
#     REDIS['default']['HOST'],
#     REDIS['default']['PORT'],
#     REDIS['default']['DB'])
# # with password
# # CACHEOPS_REDIS = "redis://:password@localhost:6379/1"

# CACHEOPS = {
#     # Automatically cache any User.objects.get() calls for 15 minutes
#     # This includes request.user or post.author access,
#     # where Post.author is a foreign key to auth.User
#     'auth.user': {'ops': 'get', 'timeout': 60*15},

#     # Automatically cache all gets and queryset fetches
#     # to other django.contrib.auth models for an hour
#     'auth.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},

#     # Cache gets, fetches, counts and exists to Permission
#     # 'all' is just an alias for ('get', 'fetch', 'count', 'exists')
#     'auth.permission': {'ops': 'all', 'timeout': 60*60},

#     # Enable manual caching on all other models with default timeout of an hour
#     # Use Post.objects.cache().get(...)
#     #  or Tags.objects.filter(...).order_by(...).cache()
#     # to cache particular ORM request.
#     # Invalidation is still automatic
#     '*.*': {'ops': (), 'timeout': 60*60},
# }


# Log

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        'hypnos': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
