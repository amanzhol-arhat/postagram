# core/utils.py — ТОЧНО по HTTP-API docs [attached_file:2]
from django.conf import settings


def get_dicebear_url(seed=None):
    """Правильный формат по документации."""
    dicebear_settings = getattr(settings, "DICEBEAR", None)
    if not dicebear_settings:
        return "https://api.dicebear.com/9.x/dylan/svg"

    seed = seed or dicebear_settings["DEFAULT_SEED"]
    style = dicebear_settings["DEFAULT_STYLE"]  # 'dylan'

    # ✅ ПРАВИЛЬНЫЙ ФОРМАТ: /style/svg?seed=... [attached_file:2]
    return f"{dicebear_settings['API_BASE']}/{style}/svg?seed={seed}"


def get_user_avatar_seed(user):
    return (
        getattr(user, "avatar_seed", None)
        or getattr(user, "username", None)
        or str(getattr(user, "id", "default"))
        or settings.DICEBEAR["DEFAULT_SEED"]
    )
