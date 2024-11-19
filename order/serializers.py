from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from order.models import BronStadion


class BronStadionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BronStadion
        fields = ('time', 'date')


class BronStadionPostSerializer(serializers.Serializer):
    brons = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        required=True
    )

    def validate_brons(self, data):
        lists = list(range(24))
        for i in data:
            if i is not lists:
                raise ValidationError("error")
        print("data:", data)
        return data
