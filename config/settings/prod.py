# config/settings/prod.py
from .base import *
import os
import dj_database_url
import tempfile
import base64

DEBUG = False

ALLOWED_HOSTS = [
    "ancient-beyond-92376-8e2c727e00de.herokuapp.com",
]

# ----- Static files (WhiteNoise) -----
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ----- Database (Heroku) -----
DATABASES["default"] = dj_database_url.config(
    default=os.getenv("DATABASE_URL"),
    conn_max_age=500,
    ssl_require=True,
)

# ===== Google Cloud Storage for MEDIA =====
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

# Your bucket name (set in Heroku Config Vars)
GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME")  # e.g. recipe-app-media

# We’re using Uniform access + bucket policy, so DO NOT use ACLs
GS_DEFAULT_ACL = None
GS_QUERYSTRING_AUTH = False            # public URLs (no signed querystrings)
GS_BLOB_CHUNK_SIZE = 256 * 1024        # optional, sensible upload chunk size

# Optional: keep uploads under a folder inside the bucket
# GS_LOCATION = "media"
# If you set GS_LOCATION above, uncomment this:
# MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/{GS_LOCATION}/"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"

# ---- Credentials via env var (Heroku-friendly) ----
# Put your service-account JSON (raw or base64) into Heroku Config Var: GCS_CREDENTIALS
_creds_raw = os.getenv("GCS_CREDENTIALS", "")
if _creds_raw:
    try:
        _json = base64.b64decode(_creds_raw).decode("utf-8")
    except Exception:
        _json = _creds_raw  # already plain JSON
    fd, _tmp = tempfile.mkstemp(prefix="gcs-", suffix=".json")
    with os.fdopen(fd, "w") as f:
        f.write(_json)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _tmp
