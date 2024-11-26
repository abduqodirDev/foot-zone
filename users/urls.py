from django.urls import path

from users.views import LoginAPIView, VerifyOtpAPIView, PostUserInfoAPIView


app_name='users'
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyOtpAPIView.as_view(), name='verify'),
    path('post-user-info/', PostUserInfoAPIView.as_view(), name='post-user-info'),
]
