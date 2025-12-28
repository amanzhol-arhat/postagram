from rest_framework import status
import pytest
from core.fixtures.user import user, another_user
from core.fixtures.post import post

@pytest.mark.django_db
class TestUserViewSet:
    endpoint = '/api/users/'

    def test_list(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_retrieve(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + str(user.public_id) + "/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.public_id.hex
        assert response.data['username'] == user.username
        assert response.data['email'] == user.email
        assert response.data['first_name'] == user.first_name
        assert response.data['last_name'] == user.last_name

    def test_create(self, client, user):
        client.force_authenticate(user=user)
        data = {}
        response = client.post(self.endpoint, data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update(self, client, user):
        client.force_authenticate(user=user)
        data = {
            "username": "test_user_updated",
        }
        response = client.patch(self.endpoint + str(user.public_id) + "/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == data["username"]
        
    def test_list_anonymous(self, client):
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_anonymous(self, client, user):
        response = client.get(self.endpoint + str(user.public_id) + "/")
        assert response.status_code == status.HTTP_200_OK

    def test_update_other_user(self, client, user, another_user):
        client.force_authenticate(user=user)
        data = {
            "username": "test_user_updated",
        }
        response = client.patch(self.endpoint + str(another_user.public_id) + "/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_retrieve_non_existent_user(self, client, user):
        client.force_authenticate(user=user)
        import uuid
        response = client.get(self.endpoint + str(uuid.uuid4()) + "/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
