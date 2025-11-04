import os
import json
from http import HTTPStatus

import requests

import dotenv
import pytest
from requests import session


@pytest.fixture(scope = "session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope = "session")
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users", json=user)
        api_users.append(response.json())
    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")



@pytest.fixture
def valid_user_data():
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "avatar": "https://example.com/avatar.png"
    }

@pytest.fixture
def created_user_data(app_url,valid_user_data):
    response = requests.post(f"{app_url}/api/users/", json=valid_user_data)
    assert response.status_code == HTTPStatus.CREATED
    created_user = response.json()

    yield created_user

    requests.delete(f"{app_url}/api/users/{created_user['id']}")

@pytest.fixture
def update_user_data():
    return {
    "email": "test_updated@example.com",
    "first_name": "Test_updated",
    "last_name": "User_updated",
    "avatar": "https://example.com/avatar2.png"
    }