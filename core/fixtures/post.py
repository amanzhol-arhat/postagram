import pytest

from core.fixtures.user import user  # noqa: F401
from core.post.models import Post


@pytest.fixture
def post(db, user):  # noqa: F811
    return Post.objects.create(author=user, body="Test Post Body")
