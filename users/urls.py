from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import LoginAPIView, VerifyOtpAPIView, PostUserInfoAPIView, UserInfoAPIView, UserLoginAPIView, \
    UserRegisterAPIView, ResendSmsAPIView, ResetPhoneNumberAPIView, VerifyResetPhoneNumberAPIView, \
    StadionAdminPhoneAPIView, StadionAdminPhoneDeleteAPIView, RefreshTokenView

app_name = 'users'
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyOtpAPIView.as_view(), name='verify'),
    path('resend-sms/', ResendSmsAPIView.as_view(), name='resend-sms'),
    path('post-user-info/', PostUserInfoAPIView.as_view(), name='post-user-info'),

    path('reset-phone-number/', ResetPhoneNumberAPIView.as_view(), name='reset-phone-number'),
    path('verify-reset-phone-number/', VerifyResetPhoneNumberAPIView.as_view(), name='verify-reset-phone-number'),

    path('user-info/', UserInfoAPIView.as_view(), name='user-info'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', RefreshTokenView.as_view(), name='refresh-token-view'),

    path('logiin/', UserLoginAPIView.as_view(), name='logiin'),
    path('register/', UserRegisterAPIView.as_view(), name='register'),

    path('phones/', StadionAdminPhoneAPIView.as_view(), name="stadion-get-post"),
    path('phones/<int:pk>/', StadionAdminPhoneDeleteAPIView.as_view(), name="stadion-delete"),
]
