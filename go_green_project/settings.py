"""
Django settings for go_green_project project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from decouple import config
#from django.contrib.auth.backends import AllowAllUsersModelBackend

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
	'admin_tools',
	'admin_tools.theming',
	'admin_tools.menu',
	'admin_tools.dashboard',
	'dal',
	'dal_select2',
	'django.contrib.admin',
	'django.contrib.sites',
	'registration',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.flatpages',
	'client',
	'widget_tweaks',
	'phonenumber_field',
	'qrcode',
	'store',
	'bills',
	'rest_framework',
	'rest_framework.authtoken',
	'django_twilio',
	'notifications',
	'apps.search',
	'bootstrap_pagination',
	'location_field.apps.DefaultConfig',
	'locator',
	'blog',
	'pos',
	'django.contrib.sitemaps',
	'robots',
	'django_extensions',
	'sorl.thumbnail',
	'djangoseo',
	'django_social_share',
	"social_widgets",
	'django_instagram',
	'guardian',
]

SITE_ID = 1

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
	messages.DEBUG: 'alert-info',
	messages.INFO: 'alert-info',
	messages.SUCCESS: 'alert-success',
	messages.WARNING: 'alert-warning',
	messages.ERROR: 'alert-danger',
}

AUTHENTICATION_BACKENDS = ( 
	'django.contrib.auth.backends.AllowAllUsersModelBackend',
	'guardian.backends.ObjectPermissionBackend',
	 )


TWITTER_FEED_CONSUMER_PUBLIC_KEY = config('TWITTER_FEED_CONSUMER_PUBLIC_KEY')
TWITTER_FEED_CONSUMER_SECRET = config('TWITTER_FEED_CONSUMER_SECRET')
TWITTER_FEED_OPEN_AUTH_TOKEN = config('TWITTER_FEED_OPEN_AUTH_TOKEN')
TWITTER_FEED_OPEN_AUTH_SECRET = config('TWITTER_FEED_OPEN_AUTH_SECRET')



ANONYMOUS_USER_NAME = None #django-gaurdian ANONYMOUS_USER_NAME, different from django anonymous_user

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; 
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.
LOGIN_REDIRECT_URL = 'profile_login'
LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = '/accounts/register/'

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'go_green_project.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [TEMPLATE_DIR, ],
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				"django.template.context_processors.i18n",
				'django.contrib.messages.context_processors.messages',
			],
			'loaders': [
				# insert your TEMPLATE_LOADERS here
				'admin_tools.template_loaders.Loader',
				'django.template.loaders.filesystem.Loader',
				'django.template.loaders.app_directories.Loader',
			]
		},
	},
]

WSGI_APPLICATION = 'go_green_project.wsgi.application'

SEO_MODELS = [
	'store.models.store',
]


#twilio

TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_DEFAULT_CALLERID = config("TWILIO_DEFAULT_CALLERID")
NO = config('NO')

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

REST_FRAMEWORK = { 
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.TokenAuthentication',
		'rest_framework.authentication.BasicAuthentication',
		'rest_framework.authentication.SessionAuthentication',
	),
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.IsAuthenticated',
	)
}

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# Notifications settings
NOTIFICATIONS_USE_JSONFIELD=True
NOTIFICATIONS_SOFT_DELETE=True


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = [STATIC_DIR, ]


#Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

# Admin site settings
from django.contrib import admin

admin.site.site_header = 'GoGreen' 
admin.site.site_title = 'GoGreen'

ADMIN_TOOLS_THEMING_CSS = 'css/theming.css'

# pone number settings
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "IN"


#for deployment

import dj_database_url
DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

DEBUG = False

try:
	from .local_settings import *
except ImportError:
	pass