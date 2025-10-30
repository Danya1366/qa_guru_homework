from http import HTTPStatus
from http.client import HTTPException

import pytest
import requests


def test_smoke_status(app_url):
    response = requests.get(f"{app_url}/status")
    print('service_available')
    data = response.json()
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    assert "users" in data, "Ответ не содержит ключ 'users'"
    assert data["users"] is True, "Сервис 'users' недоступен"