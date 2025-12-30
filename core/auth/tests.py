import pytest
from rest_framework import status

from core.fixtures.user import user  # noqa: F401


@pytest.mark.django_db
class TestAuthenticationViewSet:
    endpoint = "/api/auth/"

    def test_login(self, client, user):  # noqa: F811
        data = {"email": user.email, "password": "test_password"}
        response = client.post(self.endpoint + "login/", data)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["id"] == user.public_id.hex
        assert response.data["user"]["username"] == user.username
        assert response.data["user"]["email"] == user.email

    def test_register(self, client):
        data = {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "test_password",
            "first_name": "John",
            "last_name": "Doe",
        }

        response = client.post(self.endpoint + "register/", data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_refresh(self, client, user):  # noqa: F811
        data = {"email": user.email, "password": "test_password"}
        response = client.post(self.endpoint + "login/", data)
        assert response.status_code == status.HTTP_200_OK

        data_refresh = {"refresh": response.data["refresh"]}

        response = client.post(self.endpoint + "refresh/", data_refresh)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_register_with_existing_email(self, client, user):  # noqa: F811
        data = {
            "username": "newuser",
            "email": user.email,  # Existing email
            "password": "new_password",
            "first_name": "New",
            "last_name": "User",
        }
        response = client.post(self.endpoint + "register/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_with_invalid_data(self, client):
        data = {
            "username": "",
            "email": "invalid-email",
            "password": "123",
        }
        response = client.post(self.endpoint + "register/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_with_invalid_credentials(self, client, user):  # noqa: F811
        data = {"email": user.email, "password": "wrong_password"}
        response = client.post(self.endpoint + "login/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_with_invalid_token(self, client):
        data = {"refresh": "invalid_token"}
        response = client.post(self.endpoint + "refresh/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
