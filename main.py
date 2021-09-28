from json.decoder import JSONDecodeError
import requests

try:
    response = requests.get("https://playground.learnqa.ru/api/get_text")
    print(response.json())
except JSONDecodeError:
    print("not json")