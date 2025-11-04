"""
Django settings for config project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# === SECURITY ===
SECRET_KEY = 'django-insecure-phqn#mi_k(dpq44jnvu+27iuoa%ws-sksj9aq+z!rv*cd+xw(7'
DEBUG = True

ALLOWED_HOSTS = [
    "outsource.sifatdev.uz",
    "127.0.0.1",
    "localhost",
    "outsource-umber.vercel.app",
    "outsourcenavoi.uz"
]

# === APPS ===
INSTALLED_APPS = [
    'jazzmin',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'drf_yasg',
    'corsheaders',  # CORS uchun
    'core',
]

# === MIDDLEWARE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # ⚠️ CORS middleware — SessionMiddleware dan keyin, CommonMiddleware dan oldin
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === CORS SETTINGS ===
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://outsource.sifatdev.uz",
    "http://outsource.sifatdev.uz",
    "https://outsource-umber.vercel.app",
    "https://outsourcenavoi.uz",
]

# Ba’zan swagger yoki testlar uchun hamma domenlardan ruxsat berish mumkin:
CORS_ALLOW_ALL_ORIGINS = False  # True qilish xavfli, lekin testda vaqtincha mumkin

# Agar kerak bo‘lsa, qo‘shimcha headerlarga ruxsat berish:
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# === CSRF TRUSTED ORIGINS ===
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://outsource.sifatdev.uz",
    "https://outsource.sifatdev.uz",
    "https://outsource-umber.vercel.app",
    "https://outsourcenavoi.uz",
]

# === URL & APPS ===
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# === DATABASE ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === PASSWORD VALIDATION ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === INTERNATIONALIZATION ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# === STATIC & MEDIA ===
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# === DEFAULT AUTO FIELD ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === REST FRAMEWORK (optional config) ===
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
