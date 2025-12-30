import pytest

from core.comment.models import Comment
from core.fixtures.post import post  # noqa: F401
from core.fixtures.user import user  # noqa: F401


@pytest.fixture
def comment(db, user, post):  # noqa: F811
    return Comment.objects.create(
        author=user, post=post, body="Test Comment Body"
    )  # noqa: E501
