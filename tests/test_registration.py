import allure
import pytest


@allure.feature("Создание пользователя")
class TestRegistration:
    @allure.title("Регистрация с уникальным email")
    def test_register_unique_user(self, register, user_data):
        response = register(user_data)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": user_data["email"], "name": user_data["name"]}
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @allure.title("Повторная регистрация с тем же email")
    @pytest.mark.usefixtures("token")
    def test_register_existing_user(self, register, user_data):
        response = register(user_data)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": "User already exists"}

    @pytest.mark.parametrize("field", ["email", "password", "name"])
    @allure.title("Регистрация без обязательного поля {field}")
    def test_register_without_required_field(self, register, user_data, field):
        del user_data[field]
        response = register(user_data)

        assert response.status_code == 403
        assert response.json() == {
            "success": False, "message": "Email, password and name are required fields",
        }
