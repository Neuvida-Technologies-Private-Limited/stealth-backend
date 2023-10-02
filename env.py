import decouple

SECRET_KEY = decouple.config("SECRET_KEY")
DEBUG = decouple.config("DEBUG", cast=bool)
JWT_TOKEN_LIFE = decouple.config("JWT_TOKEN_LIFE", cast=int)
JWT_SLIDING_REFRESH_LIFETIME = decouple.config("JWT_SLIDING_REFRESH_LIFETIME", cast=int)
JWT_SLIDING_LIFETIME = decouple.config("JWT_SLIDING_LIFETIME", cast=int)
JWT_GRACE = decouple.config("JWT_GRACE", cast=int)
EMAIL = decouple.config("EMAIL")
EMAIL_PASSWORD = decouple.config("EMAIL_PASSWORD")
MYSQL_DATABASE = decouple.config("DB_NAME")
MYSQL_USER = decouple.config("DB_USERNAME")
MYSQL_ROOT_PASSWORD = decouple.config("DB_PASSWORD")
MYSQL_PASSWORD = decouple.config("DB_PASSWORD")
MYSQL_PORT = decouple.config("DB_PORT")
MYSQL_HOST = decouple.config("DB_HOST")
FERNET_KEY = decouple.config("FERNET_KEY")
EMAIL_HOST_USER = decouple.config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = decouple.config("EMAIL_HOST_PASSWORD")
CORS_ALLOW_ALL_ORIGINS = decouple.config("CORS_ALLOW_ALL_ORIGINS", cast=bool)
CORS_ALLOW_CREDENTIALS = decouple.config("CORS_ALLOW_CREDENTIALS", cast=bool)
GOOGLE_OAUTH2_CLIENT_ID = decouple.config("GOOGLE_OAUTH2_CLIENT_ID")
GOOGLE_ID_TOKEN_INFO_URL = decouple.config("GOOGLE_ID_TOKEN_INFO_URL")
EMAIL_HOST_USER_EMAIL = decouple.config("EMAIL_HOST_USER_EMAIL")