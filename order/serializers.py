from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from order.models import BronStadion
from order.utils import format_time
from stadion.models import Stadion
from stadion.serializers import StadionSerializer
from users.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number')


class BronStadionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BronStadion
        fields = ('id', 'time') # date olib tashlandi

    def to_representation(self, instance):
        data = super(BronStadionSerializer, self).to_representation(instance)
        time = data.get('time', None)
        if time:
            data['time'] = format_time(time)
        return data


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


class MyBronstadionSerializer(serializers.ModelSerializer):
    stadion = StadionSerializer()
    class Meta:
        model = BronStadion
        fields = ('id', 'stadion', 'time', 'date', 'status', 'is_active')

    def to_representation(self, instance):
        data = super(MyBronstadionSerializer, self).to_representation(instance)
        time = data.get('time', None)
        if time:
            data['time'] = format_time(time)
        return data


class MyStadionBronSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    class Meta:
        model = BronStadion
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        time = data.get('time', None)
        if time:
            data['time'] = format_time(time)
        stadion_id = data.get('stadion', None)
        data['stadion'] = Stadion.objects.get(id=stadion_id).title
        return data


class VerifyBronSerializer(serializers.Serializer):
    bron_id = serializers.IntegerField(min_value=0, required=True)
    is_active = serializers.BooleanField(required=True)

