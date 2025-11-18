from http import HTTPStatus
from http.client import HTTPException

import pytest
import requests


def test_smoke_status(status_api):
    response = status_api.get_status()
    print('service_available')
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    data = response.json()
    assert "database" in data, "Ответ не содержит ключ 'database'"
    assert data["database"] is True, "'Сервис базы данных' недоступен"
