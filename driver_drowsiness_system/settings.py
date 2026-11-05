import os
import ssl
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-development-only-key')

DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

# Allowed hosts configuration supporting Render, Railway, localhost, and custom domains
ALLOWED_HOSTS = [host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if host.strip()]

for default_host in ['healthcheck.railway.app', '.onrender.com', 'localhost', '127.0.0.1']:
    if default_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(default_host)

# Render provides RENDER_EXTERNAL_HOSTNAME automatically
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF trusted origins for web requests
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()]
if 'https://*.onrender.com' not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append('https://*.onrender.com')
if RENDER_EXTERNAL_HOSTNAME:
    render_origin = f'https://{RENDER_EXTERNAL_HOSTNAME}'
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Channels for WebSocket support
    'channels',

    'apps.accounts',
    'apps.detection',
    'apps.alerts',
    'apps.reports',
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'driver_drowsiness_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'driver_drowsiness_system.wsgi.application'
ASGI_APPLICATION = 'driver_drowsiness_system.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Database configuration: MySQL (via DATABASE_URL or individual env vars) with SQLite fallback
def configure_databases():
    db_url = os.environ.get('DATABASE_URL', '').strip()

    # 1. Try parsing DATABASE_URL if provided and free of unreplaced template brackets (<...>)
    if db_url and not ('<' in db_url or '>' in db_url):
        try:
            import dj_database_url
            database_config = dj_database_url.parse(db_url, conn_max_age=600, conn_health_checks=True)
            if database_config.get('ENGINE') == 'django.db.backends.mysql':
                options = database_config.setdefault('OPTIONS', {})
                options['charset'] = 'utf8mb4'
                # PyMySQL requires 'ssl' to be a dict or SSLContext, not string 'ssl-mode'
                ssl_mode = options.pop('ssl-mode', None) or options.pop('sslmode', None) or os.environ.get('MYSQL_SSL')
                if ssl_mode or os.environ.get('MYSQL_SSL_CA') or 'ssl-mode=REQUIRED' in db_url or 'tidbcloud.com' in db_url:
                    options['ssl'] = ssl.create_default_context()
            return {'default': database_config}
        except Exception as e:
            print(f"[WARNING] Could not parse DATABASE_URL ({e}). Checking individual MySQL variables...")

    # 2. Check for individual MySQL environment variables (e.g. TiDB, Aiven, RDS)
    mysql_host = os.environ.get('MYSQL_HOST') or os.environ.get('DB_HOST')
    mysql_db = os.environ.get('MYSQL_DATABASE') or os.environ.get('DB_NAME') or os.environ.get('MYSQL_DB')
    if mysql_host:
        raw_port = os.environ.get('MYSQL_PORT') or os.environ.get('DB_PORT', '4000' if 'tidbcloud' in mysql_host else '3306')
        try:
            port = int(raw_port)
        except (ValueError, TypeError):
            port = 4000 if 'tidbcloud' in mysql_host else 3306

        mysql_options = {'charset': 'utf8mb4'}
        if os.environ.get('MYSQL_SSL', 'true').lower() in ('true', '1', 'yes') or 'tidbcloud' in mysql_host:
            mysql_options['ssl'] = ssl.create_default_context()

        return {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': mysql_db or 'sys',
                'USER': os.environ.get('MYSQL_USER') or os.environ.get('DB_USER', 'root'),
                'PASSWORD': os.environ.get('MYSQL_PASSWORD') or os.environ.get('DB_PASSWORD', ''),
                'HOST': mysql_host,
                'PORT': port,
                'CONN_MAX_AGE': 600,
                'CONN_HEALTH_CHECKS': True,
                'OPTIONS': mysql_options,
            }
        }

    if db_url and ('<' in db_url or '>' in db_url):
        print("[WARNING] DATABASE_URL contains placeholder '<...>' characters! Using SQLite fallback for build.")

    return {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

DATABASES = configure_databases()

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Detection state is short-lived and changes for every video frame.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'drowsiness-runtime',
        'TIMEOUT': 60 * 60,
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
