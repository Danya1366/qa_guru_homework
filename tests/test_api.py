import json
from http import HTTPStatus

import pytest
import requests
from app.models.User import User



@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()

@pytest.mark.usefixtures("fill_test_data")
def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    users_list = data["items"]
    for user in users_list:
        User.model_validate(user)


def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users["items"]]
    assert len(users_ids) == len(set(users_ids))


def test_user(app_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)


# @pytest.mark.usefixtures("fill_test_data")
def test_user_nonexistent_values(app_url, fill_test_data):
    max_existing_id = max(fill_test_data) if fill_test_data else 0
    nonexistent_id = max_existing_id + 1
    response = requests.get(f"{app_url}/api/users/{nonexistent_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
