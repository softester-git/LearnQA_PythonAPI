import pytest
import requests
import allure
from lib.base_case import BaseCase


@allure.epic("Authorization cases")
class TestPasswordSelection(BaseCase):
    url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
    check_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
    password = []
    with open('passwords.txt') as f:
        password = f.read().splitlines()

    @allure.epic("Authorization cases")
    @allure.feature("Login user")
    @allure.story("Password selection")
    @pytest.mark.parametrize("password", password)
    def test_password_selection(self, password):
        data = {
            "login": "super_admin",
            "password": password
        }
        response = requests.post(url=self.url, data=data)
        cookie = self.get_cookie(response, "auth_cookie")
        response_check = requests.post(url=self.check_url, cookies={"auth_cookie": cookie})
        assert response_check.content.decode("utf-8") == f"You are NOT authorized", f"Password found! '{password}'"

