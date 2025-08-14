# --- inside config/settings/prod.py ---

from .base import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [
    "ancient-beyond-92376-8e2c727e00de.herokuapp.com",
]

# WhiteNoise for STATIC (keep yours)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES["default"] = dj_database_url.config(
    conn_max_age=500, ssl_require=True, default=os.getenv("DATABASE_URL")
)

# ---------------------------
# Cloudinary for MEDIA files
# ---------------------------
INSTALLED_APPS += [
    "cloudinary",
    "cloudinary_storage",
]

# Use Cloudinary for MEDIA storage
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Configure from Heroku env vars
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    # optional: put uploads into a folder in your Cloudinary account
    # "PREFIX": "recipes",
}

# Cloudinary returns absolute URLs; MEDIA_URL can be anything
MEDIA_URL = "/media/"
