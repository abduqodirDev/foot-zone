from django.shortcuts import render
from rest_framework.generics import ListAPIView

from useradmin.serializers import UserSerializer
from users.models import User


class ListStadionAdminAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(role='A')


class ListCommonUserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(role='C')
