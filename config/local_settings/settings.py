import env

from config.base import *

#  WARNINGSECURITY: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = [
    "127.0.0.1",
]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware"  # django debug toolbar middleware
]
ALLOWED_HOSTS = ["*"]

SECRET_KEY = env.SECRET_KEY

# Database
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env.MYSQL_DATABASE,
        "USER": env.MYSQL_USER,
        "MASTER_USER": env.MYSQL_USER,
        "PASSWORD": env.MYSQL_PASSWORD,
        "HOST": env.MYSQL_HOST,
        "PORT": env.MYSQL_PORT,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

BASE_URL = "http://127.0.0.1:8000"