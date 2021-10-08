from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):

    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post("/user/login", data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        response0 = MyRequests.delete(f"/user/2",
                                 cookies={"auth_sid": auth_sid},
                                 headers={"x-csrf-token": token})
        print(response0.status_code)
        print(response0.content.decode("utf-8"))
        Assertions.assert_code_status(response0, 400)
        assert response0.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5."

    def test_positive_delete_case(self):
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
        response0 = MyRequests.delete(f"/user/{user1_id}",
                                 cookies={"auth_sid": auth_sid},
                                 headers={"x-csrf-token": token})

        response3 = MyRequests.get(f"/user/{user1_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response3, 404)
        assert response3.content.decode("utf-8") == f"User not found"

    def test_negative_delete_case(self):
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

        # Try to delete second user
        response3 = MyRequests.delete(f"/user/{user1_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        response4 = MyRequests.get(f"/user/{user1_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_has_key(response4, "username")
