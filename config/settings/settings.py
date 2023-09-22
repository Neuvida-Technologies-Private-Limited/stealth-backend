import env

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.DEBUG  # os.getenv('DEBUG')

if DEBUG:
    # configuration for django debug toolbar
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware"  # django debug toolbar middleware
    ]
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '_sb7l*jg2bhk=bp1hfas2q45#iv6ph_u^@dc%*jz&89(q%*!6(fzn'

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
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env.MYSQL_DATABASE,
        'USER': env.MYSQL_USER,
        'MASTER_USER': env.MYSQL_USER,
        'PASSWORD': env.MYSQL_PASSWORD,
        'HOST': env.MYSQL_HOST,
        'PORT': env.MYSQL_PORT,
    }
}
