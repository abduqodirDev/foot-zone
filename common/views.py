from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from common.models import LikedStadion
from common.serializers import LikedStadionSerializer


class LikedStadionView(ListAPIView):
    serializer_class = LikedStadionSerializer
    queryset = LikedStadion.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
