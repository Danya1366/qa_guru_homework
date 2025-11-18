from http import HTTPStatus

import requests
from fastapi_pagination import response

from tests.conftest import valid_user_data, update_user_data


def test_user_flow(users_api, valid_user_data, update_user_data):
    response_create = users_api.create_user(valid_user_data)
    assert response_create.status_code == HTTPStatus.CREATED
    created_user = response_create.json()

    response_read = users_api.get_user(created_user["id"])
    assert  response_read.status_code == HTTPStatus.OK

    response_patch = users_api.update_user(created_user["id"], update_user_data)
    assert response_patch.status_code == HTTPStatus.OK

    response_delete = users_api.delete_user(created_user["id"])
    assert response_delete.status_code == HTTPStatus.OK

def test_get_after_delete(users_api,created_user_data, valid_user_data):
    created_user_id = created_user_data["id"]
    users_api.delete_user(created_user_id)
    response_get_deleted = users_api.get_user(created_user_id)
    assert response_get_deleted.status_code == HTTPStatus.NOT_FOUND

def test_create_user_invalid_email(users_api, valid_user_data,created_user_data):
    created_user_id = created_user_data["id"]
    invalid_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "email",
        "avatar": "https://example.com/avatar.png"
    }
    response_patch = users_api.update_user(created_user_id, invalid_data)
    assert response_patch.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    users_api.delete_user(created_user_id)