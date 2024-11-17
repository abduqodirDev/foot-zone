from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from stadion.models import Stadion
from stadion.serializers import StadionSerializer, StadionDetailSerializer


class StadionListAPIView(ListAPIView):
    queryset = Stadion.objects.all()
    serializer_class = StadionSerializer


class DetailStadionAPIView(RetrieveAPIView):
    queryset = Stadion.objects.all()
    serializer_class = StadionDetailSerializer
    lookup_url_kwarg = "id"
