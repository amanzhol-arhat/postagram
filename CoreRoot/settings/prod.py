import dj_database_url

from .base import *  # noqa: F403, F405

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")  # noqa: F405


CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")  # noqa: F405


DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=False)}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
