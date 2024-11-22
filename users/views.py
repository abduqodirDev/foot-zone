import uuid
from datetime import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, VerificationOtp
from users.serializers import LoginSerializer
from users.validators import create_otp_code


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    http_method_names = ['post']

    @staticmethod
    def check_verify_otp_code(user):
        verifies = user.verificationotps.all()
        if verifies.filter(expires_time__gte=datetime.now()).exists():
            return False
        else:
            return True
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            context = {
                'status': False,
                'message': 'Invalid_data'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        phone_number = data['phone_number']

        try:
            user = User.objects.get(phone_number=phone_number)
            if self.check_verify_otp_code(user):
                code = create_otp_code()
                VerificationOtp.objects.create(user=user, code=code)
                context = {
                    'status': True,
                    'message': 'code yuborildi',
                    'user_new': False,
                    'user_id': user.id,
                }
                return Response(context)
            else:
                context = {
                    'status': False,
                    'message': 'OTP code allaqachon yuborilgan!!!'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            random = str(uuid.uuid4())[0]

            username = f"footzone-username-{random}"
            while True:
                if User.objects.filter(username=username).exists():
                    random = str(uuid.uuid4())[0]
                    username = f"footzone-username-{random}"
                else:
                    break

            password = f"footzone-password-{random}"
            while True:
                if User.objects.filter(password=password).exists():
                    random = str(uuid.uuid4())[0]
                    password = f"footzone-password-{random}"
                else:
                    break

            user = User.objects.create(phone_number=phone_number, username=username, password=password, is_active=False)
            user.set_password(password)
            user.save()
            if self.check_verify_otp_code(user):
                code = create_otp_code()
                VerificationOtp.objects.create(user=user, code=code)
                context = {
                    'status': True,
                    'message': 'code yuborildi',
                    'user_new': True,
                    'user_id': user.id,
                }
                return Response(context)
            else:
                context = {
                    'status': False,
                    'message': 'OTP code allaqachon yuborilgan!!!'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

