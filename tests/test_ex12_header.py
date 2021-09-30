import requests

def test_headers():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    print(response.headers)
    print(response.headers["x-secret-homework-header"])
    assert response.headers["x-secret-homework-header"] == "Some secret value", f"Header 'x-secret-homework-header' does not have value 'Some secret value'"
