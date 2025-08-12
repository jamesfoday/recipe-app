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

# Allowed hosts - add your Heroku app domain here WITHOUT protocol or trailing slash
ALLOWED_HOSTS = [
    'ancient-beyond-92376-8e2c727e00de.herokuapp.com',  # just the domain
    'localhost',  # optional for local testing
]

# Static files (CSS, JavaScript, Images)

STATIC_ROOT = BASE_DIR / 'staticfiles'  # directory where collectstatic will collect files
STATIC_URL = '/static/'

# Add WhiteNoise middleware for serving static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files
    *MIDDLEWARE[1:],  # keep rest of the middleware from base.py
]

# Use WhiteNoise's compressed manifest static files storage for better performance
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database configuration for production (Heroku/Postgres)
DATABASES['default'].update(
    dj_database_url.config(conn_max_age=500, ssl_require=True)
)

# Other production-specific settings can be added here as needed

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
