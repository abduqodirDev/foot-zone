from random import randint

from django.core.exceptions import ValidationError


def check_phone_validator(obj):
    if not obj.startswith('+998') or len(obj) != 13 or not obj[1:].isdigit():
        raise ValidationError(message="phone number is not valid")
    else:
        return True


def check_code_validator(obj):
    if not str(obj).isdigit() or len(str(obj)) != 4:
        raise ValidationError(message="OTP code is invalid")


def create_otp_code():
    code = ''.join(str(randint(0, 9)) for _ in range(4))

    return code
