from uuid import uuid4

import pytest
import requests


@pytest.fixture
def api():
    with requests.Session() as session:
        def send(method, path, *, token=None, json=None):
            headers = {"Authorization": token} if token else {}
            return session.request(
                method, f"https://qa-stellarburgers.education-services.ru/api/{path}",
                json=json, headers=headers, timeout=30,
            )

        yield send


@pytest.fixture
def user_data():
    return {
        "email": f"stellar-{uuid4().hex}@example.com",
        "password": uuid4().hex,
        "name": "Тестовый пользователь",
    }


@pytest.fixture
def register(api):
    tokens = []

    def create(data):
        response = api("POST", "auth/register", json=data)
        if response.ok:
            tokens.append(response.json()["accessToken"])
        return response

    yield create

    for token in tokens:
        api("DELETE", "auth/user", token=token).raise_for_status()


@pytest.fixture
def token(register, user_data):
    response = register(user_data)
    response.raise_for_status()
    return response.json()["accessToken"]


@pytest.fixture
def ingredient_ids(api):
    response = api("GET", "ingredients")
    response.raise_for_status()
    catalog = response.json()["data"]
    return [next(item["_id"] for item in catalog if item["type"] == kind)
            for kind in ("bun", "main")]


@pytest.fixture
def order_number(api, token, ingredient_ids):
    response = api("POST", "orders", token=token, json={"ingredients": ingredient_ids})
    response.raise_for_status()
    return response.json()["order"]["number"]
