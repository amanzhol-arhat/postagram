from core.abstract import AbstractViewSet
from core.auth.permission import UserPermission

from .models import User
from .serializers import UserSerializer


class UserViewSet(AbstractViewSet):
    http_method_names = ["patch", "get"]
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
