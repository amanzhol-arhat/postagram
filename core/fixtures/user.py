import pytest
from core.user.models import User


data_user = {
    "username": "test_user",
    "email": "test@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "test_password"
}

@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(**data_user)

@pytest.fixture
def another_user(db) -> User:
    data_user = {
        "username": "another_user",
        "email": "another@gmail.com",
        "first_name": "Another",
        "last_name": "User",
        "password": "another_password"
    }
    return User.objects.create_user(**data_user)