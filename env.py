from decouple import config

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool)
JWT_TOKEN_LIFE = config("JWT_TOKEN_LIFE", cast=int)
JWT_SLIDING_REFRESH_LIFETIME = config("JWT_SLIDING_REFRESH_LIFETIME", cast=int)
JWT_SLIDING_LIFETIME = config("JWT_SLIDING_LIFETIME", cast=int)
JWT_GRACE = config("JWT_GRACE", cast=int)
EMAIL = config("EMAIL")
EMAIL_PASSWORD = config("EMAIL_PASSWORD")
