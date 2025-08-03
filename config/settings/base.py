from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False  # Override in `dev.py`

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.core',
    "django_ckeditor_5",
    'apps.user_data',
    'apps.ai_assistant',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Shared Production DB for all envs
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ.get("DB_PORT", "5432"),  # port can be optional
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_TZ = True
TIME_ZONE = 'UTC'  

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ["GOOGLE_CLIENT_ID"],
            'secret': os.environ["GOOGLE_SECRET"],
            'key': ''
        }
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_METHODS = {"email"}  

ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
    "password2*"
]  
ACCOUNT_ADAPTER = 'apps.accounts.adapter.NoUsernameAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'apps.accounts.adapter.MySocialAccountAdapter'

SITE_DOMAIN = 'https://faststart.in'
SITE_NAME = 'faststart'

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|",
            "bold", "italic", "underline", "strikethrough", "highlight", "fontColor", "fontBackgroundColor", "|",
            "link", "blockQuote", "code", "codeBlock", "subscript", "superscript", "|",
            "bulletedList", "numberedList", "todoList", "|",
            "outdent", "indent", "alignment", "|",
            "imageUpload", "insertImage", "mediaEmbed", "insertTable", "|",
            "htmlEmbed", "sourceEditing", "|",
            "undo", "redo", "removeFormat", "horizontalLine"
        ],
        "language": "en",
    }
}
