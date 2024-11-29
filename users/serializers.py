from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


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


class VerifyOtpSerializer(serializers.Serializer):
    user_new = serializers.BooleanField(required=True)
    user_id = serializers.IntegerField(required=True)
    code = serializers.CharField(required=True)
    brons = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        allow_empty=False,
        required=False
    )

    def validate(self, data):
        user_id = data['user_id']
        user_new = data['user_new']
        code = data['code']
        brons = data.get('brons', None)
        context = {
            'status': False,
            'message': 'Invalid_data'
        }
        if user_id < 0:
            raise ValidationError(context)

        if len(code) != 4 or not str(code).isdigit():
            raise ValidationError(context)

        if user_new and "brons" in data:
            raise ValidationError(context)

        return data


class PostUserInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, required=True)
    surname = serializers.CharField(max_length=30, required=True)
    user_id = serializers.IntegerField(required=True)
    brons = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        allow_empty=False,
        required=False
    )


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'middle_name', 'date_of_birth', 'sex', 'email', 'phone_number')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'password')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'password')
