import os

import dj_database_url

from .base import *  # noqa: F403, F405

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

if os.environ.get("TESTING") == "True":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        # Для Docker разработки (Postgres)
        DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
    else:
        # Fallback на SQLite, если запускаешь без докера
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
            }
        }

LOG_FILE_PATH = os.path.join(BASE_DIR, "django_debug.log")  # noqa: F405
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
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOG_FILE_PATH,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
