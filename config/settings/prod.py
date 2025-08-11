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

# Add your domain or Heroku app URL here
ALLOWED_HOSTS = [
    'https://ancient-beyond-92376-8e2c727e00de.herokuapp.com/',  
]

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Add WhiteNoise middleware for serving static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files
    *MIDDLEWARE[1:],  # Keep the rest of the middleware from base.py
]

# Database configuration for production (Heroku/Postgres)
DATABASES['default'].update(
    dj_database_url.config(conn_max_age=500, ssl_require=True)
)

# Optional: Use WhiteNoise's compressed manifest static files storage for performance
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
