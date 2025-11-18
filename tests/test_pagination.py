
from http import HTTPStatus

import pytest

from tests.conftest import fill_test_data, users_api


def test_total(users_api, fill_test_data):
    response = users_api.get_users()
    assert response.status_code == HTTPStatus.OK
    total = response.json()
    assert total["total"] == len(fill_test_data)

@pytest.mark.parametrize("size", [1, 7, 12])
def test_pages_depending_on_size(users_api, size):
    response = users_api.get_users(size=size)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data["items"]) == size
    assert data["size"] == size
    assert data["pages"] == ((data["total"] + size - 1) // size)

@pytest.mark.parametrize("size", [0])
def test_pages_depending_on_size_invalid_value(users_api, size):
    response = users_api.get_users(size=size)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("page", [1, 3, 4, 999])
def test_different_data_for_different_page(users_api, page):
    response = users_api.get_users(page=page, size=5)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    if page < 3:
        assert data["pages"] == ((data["total"]+5-1)//5) # 5 - size страницы
    elif page > 3:
        assert data["items"] == []

@pytest.mark.parametrize("page", [0])
def test_different_data_for_different_page_nonexistent(users_api, page):
    response = users_api.get_users(page = page)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

