from .base import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [
    "ancient-beyond-92376-8e2c727e00de.herokuapp.com",
]

# WhiteNoise for STATIC
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database from Heroku
DATABASES["default"] = dj_database_url.config(
    conn_max_age=500, ssl_require=True, default=os.getenv("DATABASE_URL")
)

# --- Cloudinary media storage (Django 5 STORAGES) ---
INSTALLED_APPS += [
    "cloudinary",
    "cloudinary_storage",
]

STORAGES = {
    "default": {  # MEDIA
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {  # STATIC (served by WhiteNoise on Heroku)
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Keep for backward compatibility, but STORAGES is the source of truth
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Cloudinary config from env
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    # IMPORTANT: provide a string prefix so the storage code can .lstrip('/') it
    "PREFIX": "media",   # or "" if you don’t want a folder; but make it a string
}

# Cloudinary returns absolute URLs; MEDIA_URL can be anything
MEDIA_URL = "/media/"

# (Keep your WhiteNoise + DB config as you already have)


# If Cloudinary URL not set but creds are, set it
cn = os.getenv("CLOUDINARY_CLOUD_NAME")
ck = os.getenv("CLOUDINARY_API_KEY")
cs = os.getenv("CLOUDINARY_API_SECRET")
if not os.getenv("CLOUDINARY_URL") and all([cn, ck, cs]):
    os.environ["CLOUDINARY_URL"] = f"cloudinary://{ck}:{cs}@{cn}"
