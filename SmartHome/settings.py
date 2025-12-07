import os
from pathlib import Path
from dotenv import load_dotenv  # <-- required for loading .env

# ------------------- Base Directory -------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------- Security -------------------
SECRET_KEY = 'your_secret_key_here'
DEBUG = True
# ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = [
    "http://192.168.31.76",
    "http://127.0.0.1",
]

ALLOWED_HOSTS = ["*"]



# ------------------- Installed Apps -------------------
INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
]

# ------------------- Middleware -------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------- URL / WSGI -------------------
ROOT_URLCONF = 'SmartHome.urls'
WSGI_APPLICATION = 'SmartHome.wsgi.application'

# ------------------- Templates -------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'home', 'templates')],
        'DIRS': [BASE_DIR / "SmartHome/home/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------- Database -------------------
# Use default SQLite database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ------------------- Password Validators -------------------
AUTH_PASSWORD_VALIDATORS = []

# ------------------- Localization -------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ------------------- Static Files -------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'home', 'static')]

# ------------------- Default Auto Field -------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------- Load Environment Variables -------------------
load_dotenv()  # ✅ Important: must come before email config

# ------------------- Email Configuration -------------------


# --- Python 3.13 Email Fix ---
import smtplib
if not hasattr(smtplib.SMTP, "_patched_for_py313"):
    _orig_starttls = smtplib.SMTP.starttls
    def _starttls(self, *args, **kwargs):
        # Ignore unsupported keyword arguments
        return _orig_starttls(self)
    smtplib.SMTP.starttls = _starttls
    smtplib.SMTP._patched_for_py313 = True
# -------------------------------- Send mail ---------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 20
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') or 'yourmail@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') or 'your-app-password'

