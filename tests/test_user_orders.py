import allure

import urls


@allure.feature("Получение заказов пользователя")
class TestUserOrders:
    @allure.title("В истории нового пользователя виден только его заказ")
    def test_get_own_orders(self, api, registered_user, created_order):
        order_number, ingredient_ids = created_order
        response = api.request("GET", urls.ORDERS, token=registered_user.token)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert [(order["number"], order["ingredients"]) for order in body["orders"]] == [
            (order_number, ingredient_ids)
        ]

    @allure.title("История заказов без авторизации")
    def test_get_orders_without_authorization(self, api):
        response = api.request("GET", urls.ORDERS)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "You should be authorised"}
