import uuid
from datetime import datetime

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from core.settings import OTP_TIME
from users.models import User, VerificationOtp, PhoneNumber
from users.permissions import StadionAdminPermission
from users.serializers import LoginSerializer, VerifyOtpSerializer, PostUserInfoSerializer, \
    UserLoginSerializer, UserRegisterSerializer, UserAdminInfoSerializer, VerifyResetPhoneNumberSerializer, \
    PhoneNumberSerializer
from users.utils import send_sms
from users.validators import create_otp_code


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    http_method_names = ['post']

    @staticmethod
    def check_verify_otp_code(user):
        if user.verificationotps.filter(expires_time__gte=datetime.now()).exists():
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
        phone_number = serializer.validated_data.get('phone_number', None)

        try:
            user = User.objects.get(phone_number=phone_number)
            if self.check_verify_otp_code(user):
                code = create_otp_code()
                VerificationOtp.objects.create(user=user, code=code)
                send_sms(phone=phone_number[1:], code=code)
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
            password = f"footzone-password-{random}"

            user = User.objects.create(phone_number=phone_number, is_active=False)
            user.set_password(password)
            user.save()
            code = create_otp_code()
            VerificationOtp.objects.create(user=user, code=code)
            send_sms(phone=phone_number[1:], code=code)
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
        user_id = data.get('user_id')
        code = data.get('code')
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
                user.is_active = True
                user.save()
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
                refresh = RefreshToken.for_user(user)
                context = {
                    'status': True,
                    'action_status': action_status,
                    'user_id': user.id,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
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
    serializer_class = UserAdminInfoSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user


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
                user = User.objects.get(phone_number=phone_number)
                user.role = "A"
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

            user = User.objects.create(
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

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class ResendSmsAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            context = {
                'status': False,
                'message': 'Invalid_data'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        phone_number = serializer.validated_data.get('phone_number', None)
        try:
            user = User.objects.get(phone_number=phone_number)
            verifies = user.verificationotps.filter(user=user, expires_time__gte=datetime.now())
            if not verifies:
                context = {
                    'status': False,
                    'message': 'Error!!!'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            if len(verifies) > 4:
                context = {
                    'status': False,
                    'message': 'Too_many_sms_sended'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            code = create_otp_code()
            VerificationOtp.objects.create(user=user, code=code)
            send_sms(phone=phone_number[1:], code=code)
            context = {
                'status': True,
                'message': 'code qayta yuborildi'
            }
            return Response(context)

        except User.DoesNotExist:
            context = {
                'status': False,
                'message': 'User_not_found'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class ResetPhoneNumberAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        user = request.user
        if not serializer.is_valid():
            context = {
                'status': False,
                'message': 'Invalid_data'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        phone_number = serializer.validated_data.get('phone_number', None)
        try:
            if User.objects.filter(phone_number=phone_number).exists():
                context = {
                    'status': False,
                    'message': "Bu nomer ro'yxatdan o'tgan"
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if user.verificationotps.filter(expires_time__gte=datetime.now()).exists():
                context = {
                    'status': False,
                    'message': 'Siz allaqachon otp code yuborib bolgansiz'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            code = create_otp_code()
            VerificationOtp.objects.create(user=user, code=code)
            send_sms(phone=phone_number[1:], code=code)
            context = {
                'status': True,
                'message': 'kod yuborildi'
            }
            return Response(context)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class VerifyResetPhoneNumberAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyResetPhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        context = {
            'status': False,
            'message': 'Invalid_data'
        }
        serializer = VerifyResetPhoneNumberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        phone_number = data.get('phone_number')
        code = data.get('code')
        try:
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

            user.phone_number = phone_number
            user.save()
            context = {
                'status': True,
                'message': 'Telefon nomer muvaffaqiyatli tasdiqlandi'
            }
            return Response(context)


        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class StadionAdminPhoneAPIView(ListCreateAPIView):
    permission_classes = [StadionAdminPermission]
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_active=True)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class StadionAdminPhoneDeleteAPIView(DestroyAPIView):
    permission_classes = [StadionAdminPermission]
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer

