import os
from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["167.71.98.235","erpdavinchy.cloud","localhost","*"]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
#
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.child('static')]

STATIC_ROOT = BASE_DIR.child('staticfiles')
MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = BASE_DIR.child('media')
#

FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760 

# EMAIL SETTINGS
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = get_secret('EMAIL')
# EMAIL_HOST_PASSWORD = get_secret('PASS_EMAIL')
# EMAIL_PORT = 587