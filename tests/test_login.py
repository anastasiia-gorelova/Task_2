import allure
import pytest

import urls
from helpers import credentials_for


@allure.feature("Логин пользователя")
class TestLogin:
    @allure.title("Вход зарегистрированного пользователя")
    def test_login_with_valid_credentials(self, api, registered_user):
        credentials = credentials_for(registered_user.data)
        response = api.request("POST", urls.LOGIN, json=credentials)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": registered_user.data["email"], "name": registered_user.data["name"]}
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @pytest.mark.parametrize("field", ["email", "password"])
    @allure.title("Вход с неверным полем {field}")
    def test_login_with_invalid_credentials(self, api, registered_user, field):
        credentials = credentials_for(registered_user.data)
        credentials[field] = "wrong-" + credentials[field]
        response = api.request("POST", urls.LOGIN, json=credentials)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "email or password are incorrect"}
