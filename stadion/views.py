from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from stadion.models import Stadion, StadionReview
from stadion.serializers import StadionSerializer, StadionDetailSerializer, StadionAddSerializer, \
    AllStadionMapSerializer, StadionImageSerializer, StadionReviewSerializer


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


class StadionImageAPIView(ListAPIView):
    serializer_class = StadionImageSerializer
    queryset = Stadion.objects.all()


class StadionReviewAPIView(ListAPIView):
    serializer_class = StadionReviewSerializer
    queryset = StadionReview.objects.all()

    def get_queryset(self):
        id = self.kwargs.get('id')
        stadion = Stadion.objects.get(id=id)
        return self.queryset.filter(stadion=stadion)
