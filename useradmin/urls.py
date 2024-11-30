from django.urls import path

from useradmin.views import ListUserAPIView

urlpatterns = [
    path('users/', ListUserAPIView.as_view(), name='users')
]
