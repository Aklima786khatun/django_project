import os
from pathlib import Path

# 1. BASE PATHS
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SECURITY SETTINGS
SECRET_KEY = "django-insecure-qg#kuysx+&cm)jp#hv(j%uuel2jcp4*7u5@1zm79za=r+%)$0r"
DEBUG = True
ALLOWED_HOSTS = []

# 3. APPLICATION DEFINITION
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app", # Your app name
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "csc_website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = "csc_website.wsgi.application"

# 4. DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 5. PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# 6. INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# 7. STATIC FILES
STATIC_URL = "static/"

# This tells Django where to look for your static files during development
STATICFILES_DIRS = [
    BASE_DIR / "app" / "static",
    r"C:\Users\acer\OneDrive\Desktop\CSCSocietyAssam\app\static",
]

# This is for production (when you run collectstatic)
STATIC_ROOT = BASE_DIR / "assets"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# This is where Django will collect all static files for production
STATIC_ROOT = os.path.join(BASE_DIR, "assets")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"