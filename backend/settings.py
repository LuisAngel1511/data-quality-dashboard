# backend/settings.py
from pathlib import Path
import os

# === Rutas base ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Clave secreta ===
# En producción, define DJANGO_SECRET_KEY en variables de entorno
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-secret-key-CHANGE-ME"
)

# === Modo debug ===
# Por defecto True en local. En Render/Railway se recomienda poner DEBUG=false en env.
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

# === Hosts permitidos ===
# Para pruebas en Render usamos '*'. En producción, pon tu dominio explícito.
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# === Confianza CSRF para Render (HTTPS) ===
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "")
if RENDER_URL:
    # Render provee una URL http://...; convertimos a https:// para CSRF
    CSRF_TRUSTED_ORIGINS = [RENDER_URL.replace("http://", "https://")]

# === Aplicaciones ===
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "rest_framework",
    "corsheaders",
    # Apps locales
    "datasets",
]

# === Middleware ===
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

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

WSGI_APPLICATION = "backend.wsgi.application"

# === Base de datos ===
# Por defecto SQLite (local). Si defines DATABASE_URL, la usamos (Render/Render Postgres).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

_db_url = os.environ.get("DATABASE_URL")
if _db_url:
    try:
        import dj_database_url  # opcional; añade a requirements si usarás Postgres
        DATABASES["default"] = dj_database_url.parse(_db_url, conn_max_age=600)
    except Exception:
        # Si no está instalado dj_database_url, nos quedamos con SQLite
        pass

# === Internacionalización ===
LANGUAGE_CODE = "es-es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# === Archivos estáticos y media ===
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# WhiteNoise para servir estáticos en producción
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# === DRF ===
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# === CORS ===
# En desarrollo permitimos todos; en prod puedes restringir con CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = True if DEBUG else True  # ajusta a tu gusto

# === Clave primaria por defecto ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
