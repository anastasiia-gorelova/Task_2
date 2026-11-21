import allure
import pytest


@allure.feature("Изменение данных пользователя")
class TestProfile:
    @pytest.mark.parametrize("field", ["email", "name"])
    @allure.title("Авторизованный пользователь меняет {field}")
    def test_update_authorized(self, api, token, user_data, field):
        new_value = "new-" + user_data[field]
        response = api("PATCH", "auth/user", token=token, json={field: new_value})

        assert response.status_code == 200
        updated = {**user_data, field: new_value}
        assert response.json() == {
            "success": True, "user": {"email": updated["email"], "name": updated["name"]},
        }

    @allure.title("После смены пароля пользователь может войти с новым паролем")
    def test_update_password(self, api, token, user_data):
        new_password = "new-" + user_data["password"]
        response = api("PATCH", "auth/user", token=token, json={"password": new_password})

        assert response.status_code == 200
        assert response.json() == {
            "success": True, "user": {"email": user_data["email"], "name": user_data["name"]},
        }
        login = api("POST", "auth/login", json={"email": user_data["email"], "password": new_password})
        assert login.status_code == 200
        assert login.json()["success"] is True

    @pytest.mark.parametrize("field", ["email", "name", "password"])
    @allure.title("Изменение поля {field} без авторизации")
    def test_update_without_authorization(self, api, user_data, field):
        response = api("PATCH", "auth/user", json={field: user_data[field]})

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "You should be authorised"}
