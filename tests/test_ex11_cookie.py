import requests

def test_cookies():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print(response.cookies)
    print(response.cookies["HomeWork"])
    assert response.cookies["HomeWork"] == "hw_value", f"Cookie 'HomeWork' does not have value 'hw_value'"
