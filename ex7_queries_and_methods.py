import requests


url = "https://playground.learnqa.ru/ajax/api/compare_query_type"


# 1
print("# 1")
response0 = requests.get(url)
response1 = requests.post(url)
response2 = requests.put(url)
response3 = requests.delete(url)
print(response0.text)
print(response1.text)
print(response2.text)
print(response3.text)


# 2
print("# 2")
#payload = {"method": "DELETE"}
#response0 = requests.head(url, data=payload)
response0 = requests.head(url)
print(response0.text)


# 3
print("# 3")
payload = {"method": "GET"}
response0 = requests.get(url, params=payload)
payload = {"method": "POST"}
response1 = requests.post(url, data=payload)
payload = {"method": "PUT"}
response2 = requests.put(url, data=payload)
payload = {"method": "DELETE"}
response3 = requests.delete(url, data=payload)
print(response0.text)
print(response1.text)
print(response2.text)
print(response3.text)


# 4
print("# 4")
method = ("GET", "POST", "PUT", "DELETE")
for m in method:
    payload = {"method": m}
    response0 = requests.get(url, params=payload)
    response1 = requests.post(url, data=payload)
    response2 = requests.put(url, data=payload)
    response3 = requests.delete(url, data=payload)
    print(f"Method {m}. Type get: {response0.text}, post: {response1.text}, put: {response2.text}, delete: {response3.text}")