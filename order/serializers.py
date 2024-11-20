from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from order.models import BronStadion


class BronStadionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BronStadion
        fields = ('time', 'date')


class BronStadionPostSerializer(serializers.Serializer):
    brons = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False,
        required=True
    )

    def validate_brons(self, brons):
        data = {
            "status": False,
            "message": "Invalid_data"
        }
        if len(brons) > 10:
            raise ValidationError(data)

        lists = [str(a) for a in range(24)]
        for dict in brons:
            if "bron" not in dict or "date" not in dict or len(dict) != 2:
                raise ValidationError(data)

            if dict["bron"] not in lists:
                raise ValidationError(data)

        return brons
