import json
from http import HTTPStatus

import pytest
import requests
from requests import session
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

# @pytest.mark.usefixtures("valid_user_data")
def test_user_create(app_url,valid_user_data):
    response = requests.post(f"{app_url}/api/users/", json=valid_user_data)
    assert response.status_code == HTTPStatus.CREATED
    created_user = response.json()
    assert "id" in created_user
    assert created_user["last_name"] == valid_user_data["last_name"]
    assert created_user["first_name"] == valid_user_data["first_name"]
    assert created_user["email"] == valid_user_data["email"]
    assert created_user["avatar"] == valid_user_data["avatar"]

    user_id = created_user["id"]
    get_response = requests.get(f"{app_url}/api/users/{user_id}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["id"] == user_id

    response_delete = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response_delete.status_code == HTTPStatus.OK

def test_delete_user(app_url, created_user_data):
    user_id = created_user_data["id"]
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert requests.get(f"{app_url}/api/users/{user_id}").status_code == HTTPStatus.NOT_FOUND

def test_patch_user(app_url, created_user_data, update_user_data):
    user_id = created_user_data["id"]
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=update_user_data)
    assert response.status_code == HTTPStatus.OK
    updated_user = response.json()
    assert updated_user["id"] == user_id
    assert updated_user["first_name"] == update_user_data["first_name"]
    assert updated_user["last_name"] == update_user_data["last_name"]
    assert updated_user["avatar"] == update_user_data["avatar"]
    assert updated_user["email"] == update_user_data["email"]

    requests.delete(f"{app_url}/api/users/{user_id}")
