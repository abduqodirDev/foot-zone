from django.urls import path

from users.views import LoginAPIView, VerifyOtpAPIView


app_name='users'
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyOtpAPIView.as_view(), name='verify'),
]
