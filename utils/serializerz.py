from rest_framework import serializers
from .models import Viloyat, Tuman


class TumanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tuman
        fields = ['id', 'name']

class ViloyatSerializer(serializers.ModelSerializer):
    tumanlar = TumanSerializer(many=True, read_only=True)

    class Meta:
        model = Viloyat
        fields = ['id', 'name', 'tumanlar']
