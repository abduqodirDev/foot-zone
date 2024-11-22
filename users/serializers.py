from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, required=True)

    def validate_phone_number(self, data):
        context = {
            'status': False,
            'message': 'Invalid_data'
        }
        if data[0] == '+':
            if str(data)[1:].isdigit:
                if data.startswith('+998') and len(str(data)) == 13:
                    pass
                elif data.startswith('+') and len(str(data)) == 10:
                    pass
                else:
                    raise ValidationError(context)
            else:
                raise ValidationError(context)
        else:
            raise ValidationError(context)

        return data
