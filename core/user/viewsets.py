from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.abstract import AbstractViewSet
from core.auth.permission import UserPermission
from core.user.models import User, UserFollow
from core.user.serializers import UserSerializer, UserSummarySerializer


class UserViewSet(AbstractViewSet):
    http_method_names = ["patch", "get", "post"]
    permission_classes = [UserPermission]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        cache_key = f"user:{instance.public_id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        serializer = self.get_serializer(instance)
        data = serializer.data

        cache.set(cache_key, data, timeout=300)

        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        cache_key = f"user:{instance.public_id}"
        cache.delete(cache_key)
        response = super().update(request, *args, **kwargs)
        cache.delete(cache_key)

        return response

    @action(detail=True, methods=["post"])
    def follow(self, request, *args, **kwargs):
        user_to_follow = self.get_object()
        current_user = request.user

        if user_to_follow == current_user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow_instance = UserFollow.objects.filter(
            user=current_user, followed=user_to_follow
        )

        if follow_instance.exists():
            follow_instance.delete()
            # Clear cache
            cache.delete(f"user:{user_to_follow.public_id}")
            cache.delete(f"user:{current_user.public_id}")
            return Response(
                {"detail": "Unfollowed", "is_following": False},
                status=status.HTTP_200_OK,
            )
        else:
            UserFollow.objects.create(user=current_user, followed=user_to_follow)
            # Clear cache
            cache.delete(f"user:{user_to_follow.public_id}")
            cache.delete(f"user:{current_user.public_id}")
            return Response(
                {"detail": "Followed", "is_following": True},
                status=status.HTTP_201_CREATED,
            )

    @action(detail=True, methods=["get"])
    def followers(self, request, *args, **kwargs):
        user = self.get_object()
        followers_qs = User.objects.filter(following__followed=user)

        page = self.paginate_queryset(followers_qs)
        if page is not None:
            serializer = UserSummarySerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = UserSummarySerializer(
            followers_qs, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def following(self, request, *args, **kwargs):
        user = self.get_object()
        following_qs = User.objects.filter(followers__user=user)

        page = self.paginate_queryset(following_qs)
        if page is not None:
            serializer = UserSummarySerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = UserSummarySerializer(
            following_qs, many=True, context={"request": request}
        )
        return Response(serializer.data)
