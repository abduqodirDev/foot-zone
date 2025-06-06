import requests
import os


token = os.getenv("BEARER")
base_url = os.getenv("BASE_URL")

def send_sms(phone, code):
    message = f"StadionTop.uz saytiga ro‘yxatdan o‘tish uchun tasdiqlash kodi: {code}"
    url = base_url
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "mobile_phone": phone,
        "message": message
    }
    requests.post(url, headers=headers, data=data)


