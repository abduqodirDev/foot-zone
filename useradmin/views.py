from django.shortcuts import render
from rest_framework.generics import ListAPIView

from useradmin.serializers import UserSerializer
from users.models import User


class ListUserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
