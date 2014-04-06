"""
Django settings for armadillo_reuse project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sfldrzlb)9iibc$-d6z%)cp4k)m!_0-%+5a%!6x@x370eid+3!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

REUSE_EMAIL_ADDRESS = 'shaladi@mit.edu'

ALLOWED_HOSTS = []

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'armadilloserver@gmail.com'
EMAIL_HOST_PASSWORD = 'arma123dillo'
DEFAULT_FROM_EMAIL = 'no-reply@reusemobile.mit.edu'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'web_api',
    'login',
    'threads'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'armadillo_reuse.urls'

WSGI_APPLICATION = 'armadillo_reuse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

ALL_DATABASES = {
    'stable': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'server_stable',
        'USER': 'web_stable',
        'PASSWORD': 'web_stable'
    },
    'unstable': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'server_unstable',
        'USER': 'web_unstable',
        'PASSWORD': 'web_unstable'
    },
    'local_test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

DATABASES = {}

# Define DATABASES dynamically

import socket

# Force use of the development database for local versions
if socket.gethostname() != "armadillo":
    DATABASES["default"] = ALL_DATABASES["local_test"]
else:
    if "unstable" in BASE_DIR:
        DATABASES["default"] = ALL_DATABASES["unstable"]
    else:
        DATABASES["default"] = ALL_DATABASES["stable"]
    

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

print DATABASES
