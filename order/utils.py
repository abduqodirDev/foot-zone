import requests
import os

from order.models import BronStadion

token = os.getenv("BEARER")
base_url = os.getenv("BASE_URL")


def format_time(time):
    time_mapping = {
        '0': '00:00-01:00',
        '1': '01:00-02:00',
        '2': '02:00-03:00',
        '3': '03:00-04:00',
        '4': '04:00-05:00',
        '5': '05:00-06:00',
        '6': '06:00-07:00',
        '7': '07:00-08:00',
        '8': '08:00-09:00',
        '9': '09:00-10:00',
        '10': '10:00-11:00',
        '11': '11:00-12:00',
        '12': '12:00-13:00',
        '13': '13:00-14:00',
        '14': '14:00-15:00',
        '15': '15:00-16:00',
        '16': '16:00-17:00',
        '17': '17:00-18:00',
        '18': '18:00-19:00',
        '19': '19:00-20:00',
        '20': '20:00-21:00',
        '21': '21:00-22:00',
        '22': '22:00-23:00',
        '23': '23:00-00:00',
    }
    return time_mapping.get(time, time)


def send_bron_sms(bron_id):
    for id in bron_id:
        bron = BronStadion.objects.filter(id=id).first()
        client_phone_number = bron.user.phone_number
        stadion = bron.stadion.title
        date = bron.date
        time = format_time(bron.time)

        message = f"{client_phone_number} telefon raqami sizning {stadion} stadiongizni {date} sana {time} vaqtda stadioningiz bron qilindi"
        user = bron.stadion.user
        phone_numbers = set()
        phone = user.phone_number
        phone_numbers.add(phone)
        numbers = user.phone_numbers.filter(is_active=True)
        for num in numbers:
            phone_numbers.add(num.phone_number)

        url = base_url
        headers = {
            "Authorization": f"Bearer {token}"
        }
        for phone in phone_numbers:
            data = {
                "mobile_phone": phone,
                "message": message,
                "from": "footzone"
            }

            requests.post(url, headers=headers, data=data)

