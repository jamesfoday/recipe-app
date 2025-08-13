from .base import *
import os
from pathlib import Path
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read environment variables from .env file (if exists)
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

# Allowed hosts - your Heroku app domain
ALLOWED_HOSTS = [
    'ancient-beyond-92376-8e2c727e00de.herokuapp.com',
    'localhost',  # optional for local testing
]

# Static files (CSS, JavaScript, Images) served by WhiteNoise
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic output dir
STATIC_URL = '/static/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files
    *MIDDLEWARE[1:],  # keep other middleware from base.py
]

# Use WhiteNoise's compressed manifest static files storage for better performance
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database config for Heroku/Postgres
DATABASES['default'].update(
    dj_database_url.config(conn_max_age=500, ssl_require=True)
)

# ---- AWS S3 CONFIGURATION FOR MEDIA UPLOADS ----
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')  # From your AWS IAM user
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')  # From your AWS IAM user
AWS_STORAGE_BUCKET_NAME = 'my-django-media-bucket-cf'  # Your S3 bucket name
AWS_S3_REGION_NAME = 'eu-north-1'  # Your AWS Region (Stockholm)
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Tell Django to use S3 for media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media settings
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
MEDIA_ROOT = ''  # Not needed when using S3 storage


