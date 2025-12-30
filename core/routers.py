from rest_framework_nested import routers

from core.auth.viewsets import LoginViewSet, RefreshViewSet, RegisterViewSet
from core.comment.viewsets import CommentViewSet
from core.post.viewsets import PostViewSet
from core.user.viewsets import UserViewSet

router = routers.SimpleRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"auth/register", RegisterViewSet, basename="auth-register")
router.register(r"auth/login", LoginViewSet, basename="auth-login")
router.register(r"auth/refresh", RefreshViewSet, basename="auth-refresh")
router.register(r"post", PostViewSet, basename="post")
posts_router = routers.NestedSimpleRouter(router, r"post", lookup="post")
posts_router.register(r"comment", CommentViewSet, basename="post-comment")


urlpatterns = [*router.urls, *posts_router.urls]
