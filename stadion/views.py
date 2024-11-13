from django.shortcuts import render
from rest_framework.generics import ListAPIView

from stadion.models import Stadion
from stadion.serializers import StadionSerializer


class StadionListAPIView(ListAPIView):
    queryset = Stadion.objects.all()
    serializer_class = StadionSerializer
