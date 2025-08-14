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

# Cloudinary for MEDIA files
INSTALLED_APPS += [
    "storages",
    "cloudinary",
    "cloudinary_storage",
]

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Let cloudinary_storage give full URLs
MEDIA_URL = None

# If Cloudinary URL not set but creds are, set it
cn = os.getenv("CLOUDINARY_CLOUD_NAME")
ck = os.getenv("CLOUDINARY_API_KEY")
cs = os.getenv("CLOUDINARY_API_SECRET")
if not os.getenv("CLOUDINARY_URL") and all([cn, ck, cs]):
    os.environ["CLOUDINARY_URL"] = f"cloudinary://{ck}:{cs}@{cn}"
