from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Local media files
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Optional: show emails in console for testing
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
