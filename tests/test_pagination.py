
from http import HTTPStatus

import pytest
import requests

def test_total(app_url):
    response = requests.get(f"{app_url}/api/users/?page=1&size=5")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["total"] == 12

@pytest.mark.parametrize("size", [1, 7, 12])
def test_pages_depending_on_size(app_url, size):
    response = requests.get(f"{app_url}/api/users/?page=1&size={size}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data["items"]) == size
    assert data["size"] == size
    assert data["pages"] == ((data["total"] + size - 1) // size)

@pytest.mark.parametrize("size", [0])
def test_pages_depending_on_size_invalid_value(app_url, size):
    response = requests.get(f"{app_url}/api/users/?page=1&size={size}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("page", [1, 3, 4, 999])
def test_different_data_for_different_page(app_url, page):
    response = requests.get(f"{app_url}/api/users/?page={page}&size=5")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    if page < 3:
        assert data["pages"] == ((data["total"]+5-1)//5) # 5 - size страницы
    elif page > 3:
        assert data["items"] == []

@pytest.mark.parametrize("page", [0])
def test_different_data_for_different_page_nonexistent(app_url, page):
    response = requests.get(f"{app_url}/api/users/?page={page}&size=5")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

