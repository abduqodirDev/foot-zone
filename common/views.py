from django.shortcuts import render
from rest_framework.generics import ListAPIView

from common.models import LikedStadion
from common.serializers import LikedStadionSerializer


class LikedStadionView(ListAPIView):
    serializer_class = LikedStadionSerializer
    queryset = LikedStadion.objects.all()
