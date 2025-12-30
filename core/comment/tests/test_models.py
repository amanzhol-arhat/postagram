import pytest

from core.comment.models import Comment
from core.fixtures.post import post  # noqa: F401
from core.fixtures.user import user  # noqa: F401


@pytest.mark.django_db
def test_create_comment(post, user):  # noqa: F811
    comment = Comment.objects.create(
        post=post, author=user, body="Test Comment Body"
    )  # noqa: E501
    assert comment.author == user
    assert comment.post == post
    assert comment.body == "Test Comment Body"
