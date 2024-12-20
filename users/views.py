import uuid
from datetime import datetime, date

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from order.models import BronStadion
from stadion.models import Stadion
from core.settings import OTP_TIME
from users.models import User, VerificationOtp
from users.serializers import LoginSerializer, VerifyOtpSerializer, PostUserInfoSerializer, UserInfoSerializer, \
    UserLoginSerializer, UserRegisterSerializer
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
                    'action_status': 'login',
                    'user_id': user.id,
                    'expire_time': OTP_TIME
                }
                return Response(context)
            else:
                context = {
                    'status': False,
                    'message': 'OTP code allaqachon yuborilgan!!!'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            random = str(uuid.uuid4()).split('-')[-1]

            username = f"footzone-username-{random}"
            while True:
                if User.objects.filter(username=username).exists():
                    random = str(uuid.uuid4())[0]
                    username = f"footzone-username-{random}"
                else:
                    break

            password = f"footzone-password-{random}"

            user = User.objects.create(phone_number=phone_number, username=username, is_active=False)
            user.set_password(password)
            user.save()
            code = create_otp_code()
            VerificationOtp.objects.create(user=user, code=code)
            context = {
                'status': True,
                'message': 'code yuborildi',
                'action_status': 'register',
                'user_id': user.id,
                'expire_time': OTP_TIME
            }
            return Response(context)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpAPIView(APIView):
    serializer_class = VerifyOtpSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwars):
        context = {
            'status': False,
            'message': 'Invalid_data'
        }
        serializer = VerifyOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user_id = data['user_id']
        code = data['code']
        try:
            user = User.objects.get(id=user_id)
            verifies = user.verificationotps.filter(expires_time__gte=datetime.now(), is_confirmed=False)
            if not verifies:
                context = {
                    'status': False,
                    'message': 'Tasdiqlash vaqtingiz tugadi'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            verify = verifies.last()
            if verify.code != code:
                context = {
                    'status': False,
                    'message': 'Code xato!!!'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            verify.is_confirmed = True
            verify.save()

            if user.is_active:
                action_status = 'login'
                refresh = RefreshToken.for_user(user)
                context = {
                    'status': True,
                    'action_status': action_status,
                    'user_id': user.id,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                action_status = 'register'
                user.is_active = True
                user.save()
                context = {
                    'status': True,
                    'action_status': action_status,
                    'user_id': user.id
                }
                return Response(context, status=status.HTTP_200_OK)


        except User.DoesNotExist:
            context = {
                'status': False,
                'message': 'User topilmadi'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class PostUserInfoAPIView(APIView):
    serializer_class = PostUserInfoSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = {
            'status': False,
            'message': 'Invalid_data'
        }
        serializer = PostUserInfoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        first_name = data.get('name', None)
        last_name = data.get('surname', None)
        user_id = data.get('user_id', None)
        try:
            user = User.objects.get(id=user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            context = {
                'status': True,
                'message': 'user malumotlari muvaffaqiyatli kiritildi',
                'user_id': user.id,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(context, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            context = {
                'status': False,
                'message': 'User not found'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPIView(RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user
    #
    # def put(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            context = {
                'status': False,
                'message': 'Invalid_data'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = serializer.validated_data
            phone_number = data.get('phone_number', None)
            password = data.get('password', None)
            user = User.objects.get(phone_number=phone_number)
            if user.role != "A":
                context = {
                    'status': False,
                    'message': 'Siz stadion admini emassiz'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                context = {
                    'status': True,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user_id': user.id,
                    'role': user.role
                }
                return Response(context)
            context = {
                'status': False,
                'message': 'Parol xato!!!'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            context = {
                'status': False,
                'message': 'User mavjud emas'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            context = {
                'status': False,
                'message': "Invalid_data"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = serializer.validated_data
            first_name = data.get('first_name', None)
            last_name = data.get('last_name', None)
            phone_number = data.get('phone_number', None)
            password = data.get('password', None)

            if User.objects.filter(phone_number=phone_number).exists():
                context = {
                    'status': False,
                    'message': 'Bu raqam avval ruyxatdan utgan'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            random = str(uuid.uuid4()).split('-')[-1]

            username = f"footzone-username-{random}"
            while True:
                if User.objects.filter(username=username).exists():
                    random = str(uuid.uuid4()).split('-')[-1]
                    username = f"footzone-username-{random}"
                else:
                    break

            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                role='A'
            )
            user.set_password(password)
            user.save()
            refresh = RefreshToken.for_user(user)
            context = {
                'status': True,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id
            }
            return Response(context)

        # except User.DoesNotExist:
        #     context = {
        #         'status': False,
        #         'message': 'Bu raqam avval ruyxatdan utgan'
        #     }
        #     return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
