import requests
import os


token = os.getenv("BEARER")
base_url = os.getenv("BASE_URL")

def send_sms(phone, code):
    # message = f"Sizning tasdiqlash kodingiz: {code}"
    message = "Bu Eskiz dan test"
    url = base_url
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "mobile_phone": phone,
        "message": message,
        "from": "footzone"
    }
    requests.post(url, headers=headers, data=data)
