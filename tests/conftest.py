from contextlib import ExitStack

import pytest
import requests

import urls
from helpers import BurgerApi, RegisteredUser, generate_user_data


@pytest.fixture
def api():
    with requests.Session() as session, ExitStack() as cleanup:
        yield BurgerApi(session, cleanup)


@pytest.fixture
def registered_user(api):
    data = generate_user_data()
    response = api.register(data)
    response.raise_for_status()
    return RegisteredUser(data, response.json()["accessToken"])


@pytest.fixture
def created_order(api, registered_user):
    ingredient_ids = api.get_ingredient_ids()
    response = api.request("POST", urls.ORDERS, token=registered_user.token,
                           json={"ingredients": ingredient_ids})
    response.raise_for_status()
    return response.json()["order"]["number"], ingredient_ids
