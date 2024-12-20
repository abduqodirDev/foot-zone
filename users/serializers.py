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
    user_id = serializers.IntegerField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, data):
        user_id = data['user_id']
        code = data['code']
        context = {
            'status': False,
            'message': 'Invalid_data'
        }

        if user_id < 0:
            raise ValidationError(context)

        if len(code) != 4 or not str(code).isdigit():
            raise ValidationError(context)

        return data


class PostUserInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, required=True)
    surname = serializers.CharField(max_length=30, required=True)
    user_id = serializers.CharField(required=True)


class UserInfoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'phone_number', 'password')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.password = validated_data.get("password", instance.password)
        if validated_data.get("password"):
            instance.set_password(validated_data.get("password"))

        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'password')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'password')
