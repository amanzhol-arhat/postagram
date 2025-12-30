import pytest
from rest_framework import status

from core.fixtures.comment import comment  # noqa: F401
from core.fixtures.post import post  # noqa: F401
from core.fixtures.user import another_user, user  # noqa: F401


@pytest.mark.django_db
class TestCommentViewSet:
    endpoint = "/api/post/{}/comment/"

    def test_list(self, client, post, comment):  # noqa: F811
        response = client.get(self.endpoint.format(post.public_id))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_create(self, client, user, post):  # noqa: F811
        client.force_authenticate(user=user)
        data = {
            "body": "Test Comment Body",
            "author": user.public_id.hex,
            "post": post.public_id.hex,
        }
        response = client.post(self.endpoint.format(post.public_id), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["body"] == data["body"]
        assert response.data["author"]["id"] == user.public_id.hex

    def test_retrieve(self, client, post, comment):  # noqa: F811
        response = client.get(
            self.endpoint.format(post.public_id) + str(comment.public_id) + "/"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == comment.public_id.hex
        assert response.data["body"] == comment.body
        assert response.data["author"]["id"] == comment.author.public_id.hex

    def test_update(self, client, user, post, comment):  # noqa: F811
        client.force_authenticate(user=user)
        data = {
            "body": "Updated Comment Body",
        }
        url = self.endpoint.format(post.public_id) + str(comment.public_id) + "/"
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["body"] == data["body"]

    def test_delete(self, client, user, post, comment):  # noqa: F811
        client.force_authenticate(user=user)
        url = self.endpoint.format(post.public_id) + str(comment.public_id) + "/"
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_anonymous(self, client, post):  # noqa: F811
        data = {
            "body": "Test Comment Body",
        }
        response = client.post(self.endpoint.format(post.public_id), data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_other_user_comment(
        self, client, another_user, post, comment
    ):  # noqa: F811
        client.force_authenticate(user=another_user)
        data = {
            "body": "Updated Comment Body",
        }
        url = self.endpoint.format(post.public_id) + str(comment.public_id) + "/"
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_other_user_comment(
        self, client, another_user, post, comment
    ):  # noqa: F811
        client.force_authenticate(user=another_user)
        url = self.endpoint.format(post.public_id) + str(comment.public_id) + "/"
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_comment_with_invalid_data(self, client, user, post):  # noqa: F811
        client.force_authenticate(user=user)
        data = {
            "body": "",
        }
        response = client.post(self.endpoint.format(post.public_id), data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_non_existent_comment(self, client, post):  # noqa: F811
        import uuid

        response = client.get(
            self.endpoint.format(post.public_id) + str(uuid.uuid4()) + "/"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
