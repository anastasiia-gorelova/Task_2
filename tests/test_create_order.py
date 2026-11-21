import allure


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Заказ с ингредиентами и авторизацией")
    def test_create_with_ingredients(self, api, token, ingredient_ids):
        response = api("POST", "orders", token=token, json={"ingredients": ingredient_ids})

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["name"]
        assert body["order"]["number"] > 0
        assert [item["_id"] for item in body["order"]["ingredients"]] == ingredient_ids

    @allure.title("Заказ с ингредиентами без авторизации")
    def test_create_without_authorization(self, api, ingredient_ids):
        response = api("POST", "orders", json={"ingredients": ingredient_ids})

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "You should be authorised"}

    @allure.title("Заказ без ингредиентов")
    def test_create_without_ingredients(self, api, token):
        response = api("POST", "orders", token=token, json={"ingredients": []})

        assert response.status_code == 400
        assert response.json() == {"success": False, "message": "Ingredient ids must be provided"}

    @allure.title("Заказ с некорректным идентификатором ингредиента")
    def test_create_with_invalid_ingredient_id(self, api, token):
        response = api("POST", "orders", token=token, json={"ingredients": ["invalid-id"]})

        assert response.status_code == 500
        assert "error" in response.text.lower()
