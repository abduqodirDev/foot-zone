from rest_framework import serializers
from common.models import LikedStadion


class LikedStadionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedStadion
        fields = "__all__"
