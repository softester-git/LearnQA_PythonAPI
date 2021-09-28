import requests


response = requests.get("https://playground.learnqa.ru/api/long_redirect")
count = len(response.history)
last = response.history[count-1].url
print(f"Количество редиректов: {count}. Итоговый URL: {last}")
