import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Edit cases")
class TestUserEdit(BaseCase):
    @allure.epic("Edit cases")
    @allure.feature("Edit users")
    @allure.story("Shorten the firstname to 1 symbol")
    def test_edit_short_firstname(self):
        data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user1_id = self.get_json_value(response1, "id")
        # User login
        data2 = {
            "email": data1["email"],
            "password": data1["password"]
        }
        response2 = MyRequests.post("/user/login", data2)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        response3 = MyRequests.put(f"/user/{user1_id}",
                                 cookies={"auth_sid": auth_sid},
                                 headers={"x-csrf-token": token},
                                 data={"firstName": "a"})
        Assertions.assert_code_status(response3, 400)

    @allure.epic("Edit cases")
    @allure.feature("Edit users")
    @allure.story("Change email to wrong value")
    def test_change_email_to_wrong_value(self):
        email = "test.com"
        data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user1_id = self.get_json_value(response1, "id")
        # User login
        data2 = {
            "email": data1["email"],
            "password": data1["password"]
        }
        response2 = MyRequests.post("/user/login", data2)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        response3 = MyRequests.put(f"/user/{user1_id}",
                                 cookies={"auth_sid": auth_sid},
                                 headers={"x-csrf-token": token},
                                 data={"email": email})
        Assertions.assert_code_status(response3, 400)

    @allure.epic("Edit cases")
    @allure.feature("Edit users")
    @allure.story("Change not user own data")
    def test_edit_another_user_data(self):
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
        # Change second users data
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user1_id}",
                                 cookies={"auth_sid": auth_sid},
                                 headers={"x-csrf-token": token},
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response3, 400)

    @allure.epic("Edit cases")
    @allure.feature("Edit users")
    @allure.story("Edit by not authorized user")
    def test_edit_by_not_authorized_user(self):
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        new_name = "Changed name"
        response2 = MyRequests.put(f"/user/{user_id}",
                                 cookies={"auth_sid": ""},
                                 headers={"x-csrf-token": ""},
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response2, 400)

        response3 = MyRequests.put(f"/user/{user_id}",
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response3, 400)


    @allure.epic("Edit cases")
    @allure.feature("Edit users")
    @allure.story("Edit just created user")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                 cookies={"auth_sid": auth_sid},
                                 headers={"x-csrf-token": token},
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(f"/user/{user_id}",
                                 cookies={"auth_sid": auth_sid},
                                 headers={"x-csrf-token": token})

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")
