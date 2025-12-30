from rest_framework import serializers

from core.abstract import AbstractSerializer

from .models import User
from .utils import get_dicebear_url, get_user_avatar_seed


class UserSerializer(AbstractSerializer):
    avatar_upload = serializers.ImageField(
        source="avatar", required=False, write_only=True
    )
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_superuser",
            "created_at",
            "updated_at",
            "avatar",
            "avatar_upload",
            "bio",
            "avatar_seed",
        ]
        read_only_fields = ["is_active", "is_superuser"]

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        seed = get_user_avatar_seed(obj)
        return get_dicebear_url(seed=seed)
