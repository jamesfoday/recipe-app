# config/settings/prod.py
from .base import *
import os
from pathlib import Path
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# -------------------------
# Env & core
# -------------------------
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = [
    "ancient-beyond-92376-8e2c727e00de.herokuapp.com",
    "localhost",
]

# -------------------------
# Static files (WhiteNoise)
# -------------------------
# Insert WhiteNoise right after SecurityMiddleware, keep the rest from base.py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *MIDDLEWARE[1:],   # comes from base.py import *
]
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------------
# Database (Heroku)
# -------------------------
DATABASES["default"].update(
    dj_database_url.config(conn_max_age=500, ssl_require=True)
)

# -------------------------
# Media on S3 (ACLs disabled / bucket-owner-enforced)
# -------------------------
USE_S3_FOR_MEDIA = True

if USE_S3_FOR_MEDIA:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    # Credentials from env
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    # ✅ Hard-set your bucket + region (env may override if present)
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "my-django-media-bucket-cf")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "eu-north-1")
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    # For bucket-owner-enforced (ACLs disabled): do NOT set 'ACL' here
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False   # public URLs (no signed querystrings)
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }

    # Public media URL
    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/"
