from rest_framework import serializers

from core.abstract.serializers import AbstractSerializer
from core.user.models import User, UserFollow

from .utils import get_dicebear_url, get_user_avatar_seed


class UserSummarySerializer(AbstractSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "bio",
        ]

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        seed = get_user_avatar_seed(obj)
        return get_dicebear_url(seed=seed)


class UserSerializer(AbstractSerializer):
    avatar_upload = serializers.ImageField(
        source="avatar", required=False, write_only=True
    )
    avatar = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

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
            "followers_count",
            "following_count",
            "is_following",
            "posts_count",
        ]
        read_only_fields = ["is_active", "is_superuser"]

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        seed = get_user_avatar_seed(obj)
        return get_dicebear_url(seed=seed)

    def get_followers_count(self, obj):
        return UserFollow.objects.filter(followed=obj).count()

    def get_following_count(self, obj):
        return UserFollow.objects.filter(user=obj).count()

    def get_is_following(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return UserFollow.objects.filter(user=request.user, followed=obj).exists()
        return False

    def get_posts_count(self, obj):
        from core.post.models import Post

        return Post.objects.filter(author=obj).count()


class UserFollowSerializer(AbstractSerializer):
    user = UserSummarySerializer(read_only=True)
    followed = UserSummarySerializer(read_only=True)

    class Meta:
        model = UserFollow
        fields = ["id", "user", "followed", "created_at"]
        read_only_fields = ["created_at"]
