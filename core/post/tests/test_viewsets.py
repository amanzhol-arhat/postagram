import pytest
from rest_framework import status

from core.fixtures.post import post  # noqa: F401
from core.fixtures.user import another_user, user  # noqa: F401


@pytest.mark.django_db
class TestPostViewSet:
    endpoint = "/api/post/"

    def test_list(self, client, user, post):  # noqa: F811
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_create(self, client, user):  # noqa: F811
        client.force_authenticate(user=user)
        data = {
            "body": "Test Post Body",
            "author": user.public_id.hex,
        }
        response = client.post(self.endpoint, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["body"] == data["body"]
        assert response.data["author"]["id"] == user.public_id.hex

    def test_retrieve(self, client, user, post):  # noqa: F811
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + str(post.public_id) + "/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == post.public_id.hex
        assert response.data["body"] == post.body
        assert response.data["author"]["id"] == post.author.public_id.hex

    def test_update(self, client, user, post):  # noqa: F811
        client.force_authenticate(user=user)
        data = {
            "body": "Test Post Body",
            "author": user.public_id.hex,
        }
        response = client.put(self.endpoint + str(post.public_id) + "/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["body"] == data["body"]

    def test_delete(self, client, user, post):  # noqa: F811
        client.force_authenticate(user=user)
        response = client.delete(self.endpoint + str(post.public_id) + "/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_list_anonymous(self, client, post):  # noqa: F811
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_retrieve_anonymous(self, client, post):  # noqa: F811
        response = client.get(self.endpoint + str(post.public_id) + "/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == post.public_id.hex
        assert response.data["body"] == post.body
        assert response.data["author"]["id"] == post.author.public_id.hex

    def test_create_anonymous(self, client):
        data = {
            "body": "Test Post Body",
            "author": "test_user",
        }
        response = client.post(self.endpoint, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_anonymous(self, client, post):  # noqa: F811
        data = {
            "body": "Test Post Body",
            "author": "test_user",
        }
        response = client.put(self.endpoint + str(post.public_id) + "/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_anonymous(self, client, post):  # noqa: F811
        response = client.delete(self.endpoint + str(post.public_id) + "/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_other_user_post(self, client, another_user, post):  # noqa: F811
        client.force_authenticate(user=another_user)
        data = {
            "body": "Test Post Body",
            "author": another_user.public_id.hex,
        }
        response = client.put(self.endpoint + str(post.public_id) + "/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_other_user_post(self, client, another_user, post):  # noqa: F811
        client.force_authenticate(user=another_user)
        response = client.delete(self.endpoint + str(post.public_id) + "/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_post_with_invalid_data(self, client, user):  # noqa: F811
        client.force_authenticate(user=user)
        data = {
            "body": "",
            "author": user.public_id.hex,
        }
        response = client.post(self.endpoint, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_non_existent_post(self, client, user):  # noqa: F811
        client.force_authenticate(user=user)
        import uuid

        response = client.get(self.endpoint + str(uuid.uuid4()) + "/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
