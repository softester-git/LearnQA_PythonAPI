import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest

@allure.epic("Create cases")
class TestUserRegister(BaseCase):
    @allure.epic("Create cases")
    @allure.feature("Register users")
    @allure.story("Register with incorrect email")
    def test_create_test_user_with_incorrect_email(self):
        email = "test.com"
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    data = [
        {
            "username": "",
            "firstName": "FirstName",
            "lastName": "LastName",
            "email": "test@test.com",
            "password": "123"
        },
        {
            "username": "UserName",
            "firstName": "",
            "lastName": "LastName",
            "email": "test@test.com",
            "password": "123"
        },
        {
            "username": "UserName",
            "firstName": "FirstName",
            "lastName": "",
            "email": "test@test.com",
            "password": "123"
        },
        {
            "username": "UserName",
            "firstName": "FirstName",
            "lastName": "LastName",
            "email": "",
            "password": "123"
        },
        {
            "username": "UserName",
            "firstName": "FirstName",
            "lastName": "LastName",
            "email": "test@test.com",
            "password": ""
        }
    ]

    @allure.epic("Create cases")
    @allure.feature("Register users")
    @allure.story("Register with missing some fields")
    @pytest.mark.parametrize("data", data)
    def test_create_user_wo_some_fields(self, data):
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)

    @allure.epic("Create cases")
    @allure.feature("Register users")
    @allure.story("Register with 1 symbol in firstname")
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data["firstName"] = "a"
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short"

    @allure.epic("Create cases")
    @allure.feature("Register users")
    @allure.story("Register with 251 symbols in firstname")
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data["firstName"] = "a"*251
        response = MyRequests.post("/user/", data=data)
        print(response.status_code)
        print(response.content)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long"


    @allure.epic("Create cases")
    @allure.feature("Register users")
    @allure.story("Register user successfully")
    @allure.description("Test cases from video lessons")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.epic("Create cases")
    @allure.feature("Register users")
    @allure.story("Register existing user")
    @allure.description("Test cases from video lessons")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"
