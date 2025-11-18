import os
import json
from http import HTTPStatus

import dotenv
import pytest
from tests.api_client import UsersApi, StatusApi

@pytest.fixture(scope = "session", autouse=True)
def envs():
    dotenv.load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope = "session")
def app_url():
    return os.getenv("APP_URL")

@pytest.fixture(scope="session")
def users_api(env):
    return UsersApi(env)

@pytest.fixture(scope="session")
def status_api(env):
    return StatusApi(env)


@pytest.fixture(scope="module")
def fill_test_data(users_api):
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = users_api.create_user(user)
        api_users.append(response.json())
    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        users_api.delete_user(user_id)



@pytest.fixture
def valid_user_data():
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "avatar": "https://example.com/avatar.png"
    }

@pytest.fixture
def created_user_data(users_api,valid_user_data):
    response = users_api.create_user(valid_user_data)
    assert response.status_code == HTTPStatus.CREATED
    created_user = response.json()

    yield created_user

    users_api.delete_user(created_user)

@pytest.fixture
def update_user_data():
    return {
    "email": "test_updated@example.com",
    "first_name": "Test_updated",
    "last_name": "User_updated",
    "avatar": "https://example.com/avatar2.png"
    }