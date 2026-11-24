from dataclasses import dataclass
from uuid import uuid4

import urls


@dataclass
class RegisteredUser:
    data: dict
    token: str


def generate_user_data():
    return {
        "email": f"stellar-{uuid4().hex}@example.com",
        "password": uuid4().hex,
        "name": "Тестовый пользователь",
    }


def credentials_for(data):
    return {"email": data["email"], "password": data["password"]}


class BurgerApi:
    def __init__(self, session, cleanup):
        self.session = session
        self.cleanup = cleanup

    def request(self, method, url, *, token=None, json=None):
        headers = {"Authorization": token} if token else {}
        return self.session.request(method, url, json=json, headers=headers, timeout=30)

    def register(self, data):
        response = self.request("POST", urls.REGISTER, json=data)
        if response.ok:
            self.cleanup.callback(self.delete_user, response.json()["accessToken"])
        return response

    def delete_user(self, token):
        self.request("DELETE", urls.USER, token=token).raise_for_status()

    def get_ingredient_ids(self):
        response = self.request("GET", urls.INGREDIENTS)
        response.raise_for_status()
        catalog = response.json()["data"]
        return [next(item["_id"] for item in catalog if item["type"] == kind)
                for kind in ("bun", "main")]
