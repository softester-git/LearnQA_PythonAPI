import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Get cases")
class TestUserGet(BaseCase):
    @allure.epic("Get data cases")
    @allure.feature("Get user data")
    @allure.story("Get not user own data")
    def test_get_data_another_user(self):
        # Create first user
        data0 = self.prepare_registration_data()
        response0 = MyRequests.post("/user/", data=data0)
        Assertions.assert_code_status(response0, 200)
        Assertions.assert_json_has_key(response0, "id")

        # Create second user
        data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user1_id = self.get_json_value(response1, "id")

        # First user login
        data2 = {
            "email": data0["email"],
            "password": data0["password"]
        }
        response2 = MyRequests.post("/user/login", data2)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        # First user try get second users data
        response3 = MyRequests.get(f"/user/{user1_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        unexpected_fields = ["email", "lastName", "firstName", "password"]
        expected_fields = ["username"]
        Assertions.assert_json_has_keys(response3, expected_fields)
        Assertions.assert_json_has_no_keys(response3, unexpected_fields)

    # From video lessons
    @allure.epic("Get data cases")
    @allure.feature("Get user data")
    @allure.story("Get data by not authorized user")
    @allure.description("Test cases from video lessons")
    def test_user_detail_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    @allure.epic("Get data cases")
    @allure.feature("Get user data")
    @allure.story("Get user own data")
    @allure.description("Test cases from video lessons")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        expected_field = ["email", "username", "lastName", "firstName"]
        print(response2.text)
        Assertions.assert_json_has_keys(response2, expected_field)
