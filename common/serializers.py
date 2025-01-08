from rest_framework import serializers
from common.models import LikedStadion, Starts
from stadion.serializers import StadionSerializer


class LikedStadionSerializer(serializers.ModelSerializer):
    stadion = StadionSerializer()
    class Meta:
        model = LikedStadion
        fields = "__all__"


class LikedStadionPostSerializer(serializers.Serializer):
    stadion_id = serializers.IntegerField(required=True, min_value=0)


class StartsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starts
        fields = ('id', 'rank', 'stadion')
