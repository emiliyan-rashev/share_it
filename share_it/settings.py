import os
from pathlib import Path
import dotenv
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = True
ALLOWED_HOSTS: list = [
    "127.0.0.1",
    "localhost",
    "54.93.85.205",
    "emiliyan-rashev.com",
    "www.emiliyan-rashev.com",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_unused_media",
    "dbbackup",
    "events",
    "expenses",
    "users",
    "utils",
]

AUTH_USER_MODEL = "users.User"

DBBACKUP_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DBBACKUP_STORAGE_OPTIONS = {
    "access_key": os.environ["DB_BACKUP_ACCESS_KEY"],
    "secret_key": os.environ["DB_BACKUP_SECRET_KEY"],
    "bucket_name": os.environ["DB_BUCKET_NAME"],
    "default_acl": "private",
}

DBBACKUP_FILENAME_TEMPLATE = "db-{datetime}.{extension}"
DBBACKUP_MEDIA_FILENAME_TEMPLATE = "media-{datetime}.{extension}"
DBBACKUP_GPG_RECIPIENT = "E3CDBA13497576271FC4B0D349038C7BB0987947"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "share_it.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "share_it.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "share_it",
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Sofia"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_FOLDER_NAME = "media"
MEDIA_URL = f"{MEDIA_FOLDER_NAME}/"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_FOLDER_NAME)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = True
EMAIL_PORT = 587
ADMINS = [(admin, admin) for admin in os.environ["ADMINS"].split("|")]
SECURE_HSTS_SECONDS = 10
SECURE_SSL_REDIRECT = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
LOGIN_URL = reverse_lazy("admin:login")
CSRF_TRUSTED_ORIGINS = ["https://emiliyan-rashev.com"]
