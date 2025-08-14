from .base import *
import os
import dj_database_url
import json, os, tempfile

DEBUG = False

ALLOWED_HOSTS = [
    "ancient-beyond-92376-8e2c727e00de.herokuapp.com",
]

# WhiteNoise
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES["default"] = dj_database_url.config(
    conn_max_age=500, ssl_require=True, default=os.getenv("DATABASE_URL")
)

# ===== Google Cloud Storage for MEDIA =====
USE_GCS_FOR_MEDIA = True

if USE_GCS_FOR_MEDIA:
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME")  # e.g. your-bucket-name

    # You set the bucket to public via IAM (allUsers → Storage Object Viewer) and
    # Uniform access is on, so **do not** use ACLs:
    GS_DEFAULT_ACL = None
    GS_QUERYSTRING_AUTH = False  # public URLs, no signed query string
    GS_BLOB_CHUNK_SIZE = 256 * 1024  # sensible default for uploads

    # Optional: keep uploads under a subfolder (purely organizational)
    # GS_LOCATION = "media"

    # MEDIA URL
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"
    # If you used GS_LOCATION, use:
    # MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/{GS_LOCATION}/"

    # ---- Credentials via env var (Heroku-friendly) ----
    # Put the JSON content into GCS_CREDENTIALS (full JSON or base64).
    creds_raw = os.getenv("GCS_CREDENTIALS", "")
    if creds_raw:
        try:
            # If base64, decode; if plain JSON, this will except and we’ll use it as-is.
            import base64
            creds_json = base64.b64decode(creds_raw).decode("utf-8")
        except Exception:
            creds_json = creds_raw

        # Write JSON to a temp file & point GOOGLE_APPLICATION_CREDENTIALS to it
        fd, tmp_path = tempfile.mkstemp(prefix="gcs-", suffix=".json")
        with os.fdopen(fd, "w") as f:
            f.write(creds_json)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tmp_path