import pytest
import requests
import json


data = [
    {
        "user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "platform": "Mobile",
        "browser": "No",
        "device": "Android"
    },
    {
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "platform": "Mobile",
        "browser": "Chrome",
        "device": "iOS"
    },
    {
        "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "platform": "Googlebot",
        "browser": "Unknown",
        "device": "Unknown"
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        "platform": "Web",
        "browser": "Chrome",
        "device": "No"
    },
    {
        "user_agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "platform": "Mobile",
        "browser": "No",
        "device": "iPhone"
    }
]

@pytest.mark.parametrize("data", data)
def test_user_agent(data):
    url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
    response = requests.get(
    "https://playground.learnqa.ru/ajax/api/user_agent_check",
    headers={"User-Agent": data["user_agent"]}
    )
    if data["platform"] in response.text:
        assert data["platform"] == json.loads(response.text)["platform"], f"Parameter 'platform' not equal '{data['platform']}' for user-agent: {data['user_agent']}"
    else:
        assert False, f"Parameter 'platform' not found in response '{response.text}'"

    if data["browser"] in response.text:
        assert data["browser"] == json.loads(response.text)["browser"], f"Parameter 'browser' not equal '{data['browser']}' for user-agent: {data['user_agent']}"
    else:
        assert False, f"Parameter 'browser' not found in response '{response.text}'"

    if data["device"] in response.text:
        assert data["device"] == json.loads(response.text)["device"], f"Parameter 'device' not equal '{data['device']}' for user-agent: {data['user_agent']}"
    else:
        assert False, f"Parameter 'device' not found in response '{response.text}'"

