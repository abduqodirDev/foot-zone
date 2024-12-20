from rest_framework import serializers
from common.models import LikedStadion
from stadion.serializers import StadionDetailSerializer, StadionSerializer


class LikedStadionSerializer(serializers.ModelSerializer):
    stadion = StadionSerializer()
    class Meta:
        model = LikedStadion
        fields = "__all__"
