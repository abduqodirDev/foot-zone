from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from order.models import BronStadion
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
        if data['status'] == 'T' and data['is_active'] == True:
            data['bron-status'] = 'Tasdiqlangan'
        elif data['status'] == 'F' and data['is_active'] == False:
            data['bron-status'] = 'Kutish'
        else:
            data['bron-status'] = 'Bekor qilingan'

        return data


class MyStadionBronSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    class Meta:
        model = BronStadion
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        time = data.get('time', None)
        if time == '0':
            data['time'] = '00.00-01.00'
        elif time == '1':
            data['time'] = '01.00-02.00'
        elif time == '2':
            data['time'] = '02.00-03.00'
        elif time == '3':
            data['time'] = '03.00-04.00'
        elif time == '4':
            data['time'] = '04.00-05.00'
        elif time == '5':
            data['time'] = '05.00-06.00'
        elif time == '6':
            data['time'] = '06.00-07.00'
        elif time == '7':
            data['time'] = '07.00-08.00'
        elif time == '8':
            data['time'] = '08.00-09.00'
        elif time == '9':
            data['time'] = '09.00-10.00'
        elif time == '10':
            data['time'] = '10.00-11.00'
        elif time == '11':
            data['time'] = '11.00-12.00'
        elif time == '12':
            data['time'] = '12:00-13.00'
        elif time == '13':
            data['time'] = '13.00-14.00'
        elif time == '14':
            data['time'] = '14.00-15.00'
        elif time == '15':
            data['time'] = '15.00-16.00'
        elif time == '16':
            data['time'] = '16:00-17.00'
        elif time == '17':
            data['time'] = '17.00-18.00'
        elif time == '18':
            data['time'] = '18.00-19.00'
        elif time == '19':
            data['time'] = '19.00-20.00'
        elif time == '20':
            data['time'] = '20:00-21.00'
        elif time == '21':
            data['time'] = '21.00-22.00'
        elif time == '22':
            data['time'] = '22.00-23.00'
        elif time == '23':
            data['time'] = '23.00-00.00'
        else:
            data['time'] = None
        return data


class VerifyBronSerializer(serializers.Serializer):
    bron_id = serializers.IntegerField(min_value=0, required=True)
    is_active = serializers.BooleanField(required=True)

