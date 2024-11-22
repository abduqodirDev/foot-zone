from random import randint

from django.core.exceptions import ValidationError


def check_phone_validator(obj):
    if obj[0] == '+':
        if str(obj)[1:].isdigit:
            if obj.startswith('+998') and len(str(obj))==13:
                return True
            elif obj.startswith('+') and len(str(obj))==10:
                return True
            else:
                raise ValidationError(message="phone number is not valid")
        else:
            raise ValidationError(message="phone number is not valid")
    else:
        raise ValidationError(message="phone number is not valid")


def check_code_validator(obj):
    if not str(obj).isdigit() or len(str(obj)) != 4:
        raise ValidationError(message="OTP code is invalid")


def create_otp_code():
    code = ''.join(str(randint(0, 9)) for _ in range(4))

    return code
