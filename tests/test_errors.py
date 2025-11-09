from http import HTTPStatus

import requests
from fastapi_pagination import response

from tests.conftest import valid_user_data, update_user_data


def test_user_flow(app_url, valid_user_data, update_user_data):
    response_create = requests.post(f"{app_url}/api/users", json=valid_user_data)
    assert response_create.status_code == HTTPStatus.CREATED
    created_user = response_create.json()

    response_read = requests.get(f"{app_url}/api/users/{created_user["id"]}")
    assert  response_read.status_code == HTTPStatus.OK

    response_patch = requests.patch(f"{app_url}/api/users/{created_user["id"]}", json=update_user_data)
    assert response_patch.status_code == HTTPStatus.OK

    response_delete = requests.delete(f"{app_url}/api/users/{created_user["id"]}")
    assert response_delete.status_code == HTTPStatus.OK

def test_get_after_delete(app_url,created_user_data, valid_user_data):
    created_user_id = created_user_data["id"]
    requests.delete(f"{app_url}/api/users/{created_user_id}")
    response_get_deleted = requests.get(f"{app_url}/api/users/{created_user_id}")
    assert response_get_deleted.status_code == HTTPStatus.NOT_FOUND

# def test_patch_nonexistent_user(app_url,created_user_data, update_user_data):
#     created_user_id = created_user_data["id"]
#     requests.delete(f"{app_url}/api/users/{created_user_id}")
#     response_patch_deleted = requests.patch(f"{app_url}/api/users/{created_user_id}", json=update_user_data)
#     assert response_patch_deleted.status_code == HTTPStatus.NOT_FOUND

def test_create_user_invalid_email(app_url, valid_user_data,created_user_data):
    created_user_id = created_user_data["id"]
    invalid_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "email",
        "avatar": "https://example.com/avatar.png"
    }
    response_patch = requests.patch(f"{app_url}/api/users/{created_user_id}", json=invalid_data)
    assert response_patch.status_code == HTTPStatus.UNPROCESSABLE_ENTITY