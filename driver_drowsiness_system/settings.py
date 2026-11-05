import os
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
if os.environ.get('DATABASE_URL'):
    db_url = os.environ.get('DATABASE_URL')
    try:
        import dj_database_url
        database_config = dj_database_url.config(conn_max_age=600, conn_health_checks=True)
    except ImportError:
        import urllib.parse
        parsed = urllib.parse.urlparse(db_url)
        engine = 'django.db.backends.mysql' if parsed.scheme in ('mysql', 'mysql2') else 'django.db.backends.sqlite3'
        database_config = {
            'ENGINE': engine,
            'NAME': parsed.path.lstrip('/'),
            'USER': parsed.username or '',
            'PASSWORD': urllib.parse.unquote(parsed.password or ''),
            'HOST': parsed.hostname or 'localhost',
            'PORT': parsed.port or 3306,
            'CONN_MAX_AGE': 600,
            'OPTIONS': {},
        }
    if database_config.get('ENGINE') == 'django.db.backends.mysql':
        options = database_config.setdefault('OPTIONS', {})
        options['charset'] = 'utf8mb4'
        # PyMySQL requires 'ssl' to be a dict or SSLContext, not string 'ssl-mode'
        ssl_mode = options.pop('ssl-mode', None) or options.pop('sslmode', None) or os.environ.get('MYSQL_SSL')
        if ssl_mode or os.environ.get('MYSQL_SSL_CA') or 'ssl-mode=REQUIRED' in db_url:
            import ssl
            options['ssl'] = ssl.create_default_context()
    DATABASES = {
        'default': database_config,
    }
elif os.environ.get('MYSQL_DATABASE') or os.environ.get('DB_NAME'):
    mysql_options = {'charset': 'utf8mb4'}
    if os.environ.get('MYSQL_SSL', 'false').lower() in ('true', '1', 'yes') or os.environ.get('DB_SSL', 'false').lower() in ('true', '1', 'yes'):
        import ssl
        mysql_options['ssl'] = ssl.create_default_context()

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQL_DATABASE') or os.environ.get('DB_NAME'),
            'USER': os.environ.get('MYSQL_USER') or os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD') or os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('MYSQL_HOST') or os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('MYSQL_PORT') or os.environ.get('DB_PORT', '3306'),
            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,
            'OPTIONS': mysql_options,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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
