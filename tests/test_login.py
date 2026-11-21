import allure
import pytest


@allure.feature("Логин пользователя")
@pytest.mark.usefixtures("token")
class TestLogin:
    @allure.title("Вход зарегистрированного пользователя")
    def test_login_with_valid_credentials(self, api, user_data):
        credentials = {key: user_data[key] for key in ("email", "password")}
        response = api("POST", "auth/login", json=credentials)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": user_data["email"], "name": user_data["name"]}
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @pytest.mark.parametrize("field", ["email", "password"])
    @allure.title("Вход с неверным полем {field}")
    def test_login_with_invalid_credentials(self, api, user_data, field):
        credentials = {key: user_data[key] for key in ("email", "password")}
        credentials[field] = "wrong-" + credentials[field]
        response = api("POST", "auth/login", json=credentials)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "email or password are incorrect"}
