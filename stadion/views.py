from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from stadion.models import Stadion
from stadion.serializers import StadionSerializer, StadionDetailSerializer, StadionAddSerializer, \
    AllStadionMapSerializer


class StadionListAPIView(ListAPIView):
    queryset = Stadion.objects.all()
    serializer_class = StadionSerializer


class DetailStadionAPIView(RetrieveAPIView):
    queryset = Stadion.objects.all()
    serializer_class = StadionDetailSerializer
    lookup_url_kwarg = "id"


class AddStadionAPIView(CreateAPIView):
    serializer_class = StadionAddSerializer
    queryset = Stadion
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllStadionMapAPIView(ListAPIView):
    serializer_class = AllStadionMapSerializer
    queryset = Stadion.objects.all()
