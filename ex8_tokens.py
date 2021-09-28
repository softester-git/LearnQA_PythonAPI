import json
import requests
from time import sleep


url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# create
response = requests.get(url)
obj = json.loads(response.text)
token = obj["token"]
seconds = obj["seconds"]

#check until deadline
payload = {"token": token}
response = requests.get(url, params=payload)
obj = json.loads(response.text)
status = obj["status"]
assert status == "Job is NOT ready"

#check after deadline
sleep(seconds+1)
response = requests.get(url, params=payload)
obj = json.loads(response.text)
status = obj["status"]
assert status == "Job is ready"
assert "result" in obj
