from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, PhoneNumber


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, required=True)

    def validate_phone_number(self, data):
        context = {
            'success': False,
            'message': 'Invalid data'
        }
        if not data.startswith('+998') or len(data) != 13 or not data[1:].isdigit():
            raise ValidationError(context)

        return data


class VerifyOtpSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, data):
        user_id = data.get('user_id')
        code = data.get('code')
        context = {
            'status': False,
            'message': 'Invalid_data'
        }

        if user_id < 0 or len(code) != 4 or not code.isdigit():
            raise ValidationError(context)

        return data


class PostUserInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, required=True)
    surname = serializers.CharField(max_length=30, required=True)
    user_id = serializers.IntegerField(required=True)


class UserAdminInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'phone_number', 'password')
        extra_kwargs = {
            "phone_number": {"required": False},
            "password": {"required": False, "write_only": True}
        }

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
        extra_kwargs = {
            'phone_number': {'validators': []},
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'password')

        extra_kwargs = {
            "phone_number": {"validators": []}
        }


class VerifyResetPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, required=True)
    code = serializers.CharField(required=True)

    def validate_phone_number(self, data):
        context = {
            'status': False,
            'message': 'Invalid_data'
        }
        if not data.startswith('+998') or len(data) != 13 or not data[1:].isdigit():
            raise ValidationError(context)

        return data


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('id', 'phone_number', 'is_active')

        extra_kwargs = {
            "user": {"required": False}
        }


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
