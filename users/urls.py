from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import LoginAPIView, VerifyOtpAPIView, PostUserInfoAPIView, UserInfoAPIView, UserLoginAPIView, \
    UserRegisterAPIView, ResendSmsAPIView

app_name = 'users'
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyOtpAPIView.as_view(), name='verify'),
    path('resend-sms/', ResendSmsAPIView.as_view(), name='resend-sms'),
    path('post-user-info/', PostUserInfoAPIView.as_view(), name='post-user-info'),

    path('user-info/', UserInfoAPIView.as_view(), name='user-info'),
    path('token/', TokenObtainPairView.as_view(), name='token'),

    path('logiin/', UserLoginAPIView.as_view(), name='logiin'),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
]
