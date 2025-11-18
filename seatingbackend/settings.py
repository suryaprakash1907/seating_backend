import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------
# SECURITY
# -------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = True   # Keep True until everything is fully working

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "seatingbackend-production.up.railway.app",
    ".railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://seatingbackend-production.up.railway.app",
    "https://*.railway.app",
]

# -------------------------------------------------------
# INSTALLED APPS
# -------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Your app
    'seating',
]

# -------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# -------------------------------------------------------
# URLS, TEMPLATES, WSGI
# -------------------------------------------------------
ROOT_URLCONF = 'seatingbackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'seatingbackend.wsgi.application'

# -------------------------------------------------------
# DATABASE (Railway PostgreSQL)
# -------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -------------------------------------------------------
# STATIC & MEDIA
# -------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------------
# REST FRAMEWORK (JWT)
# -------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# -------------------------------------------------------
# FIX ADMIN 403 on Railway
# -------------------------------------------------------
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
