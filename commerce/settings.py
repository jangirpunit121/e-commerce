from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SECRET KEY (env se lena better hota hai)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-temp-key')

# ❌ Production me False hona chahiye
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ✅ Hosts
ALLOWED_HOSTS = ['*']   # deploy ke baad domain daal dena

# ❌ '*' allowed nahi hota production me
CSRF_TRUSTED_ORIGINS = [
    "https://*.up.railway.app",
    "https://*.vercel.app"
]

# ------------------ APPS ------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'shop',

    'rest_framework',
    'rest_framework.authtoken',
]

# ------------------ MIDDLEWARE ------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Static files ke liye
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------ URLs ------------------

ROOT_URLCONF = 'commerce.urls'

WSGI_APPLICATION = 'commerce.wsgi.application'

# ------------------ DATABASE ------------------

# 🔥 Production ke liye PostgreSQL use karna (optional)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # abhi ke liye ok
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------ STATIC ------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ------------------ REST FRAMEWORK ------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}