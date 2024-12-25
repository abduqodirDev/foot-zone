from rest_framework import serializers

from stadion.models import Stadion, Images, StadionReview
from users.models import User


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('id', 'image')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadionReview
        fields = ('user', 'comment', 'created_at')


class StadionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number')


class StadionSerializer(serializers.ModelSerializer):
    star = serializers.SerializerMethodField("get_star")
    class Meta:
        model = Stadion
        fields = ['id', 'title', 'address', 'price', 'photo', 'star']

    def get_star(self, obj):
        count = 0
        starts = obj.StadionStarts.all()
        if len(starts) == 0:
            return 0
        for star in starts:
            count += star.rank
        return count / len(starts)


class StadionDetailSerializer(serializers.ModelSerializer):
    user = StadionUserSerializer()
    star = serializers.SerializerMethodField("get_star")
    class Meta:
        model = Stadion
        fields = "__all__"

    def get_star(self, obj):
        count = 0
        starts = obj.StadionStarts.all()
        if len(starts) == 0:
            return 0
        for star in starts:
            count += star.rank
        return count / len(starts)


    def to_representation(self, instance):
        data = super(StadionDetailSerializer, self).to_representation(instance)
        images = instance.images.all()
        data['images'] = ImageSerializer(images, many=True).data
        request = self.context.get('request')
        if data['images']:
            for dic in data['images']:
                dic['image'] = request.build_absolute_uri(dic['image'])
        reviews = instance.stadionreviews.all()
        data['reviews'] =ReviewSerializer(reviews, many=True).data
        return data


class StadionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadion
        fields = "__all__"
        extra_kwargs = {
            'description': {'required': False},
            'price': {'required': False},
            'title': {'required': False},
        }


class AllStadionMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadion
        fields = ('id', 'title', 'latitude', 'longitude')


class StadionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadion
        fields = ('id', 'photo')


class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'photo', 'first_name', 'last_name')


class StadionReviewSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer()
    class Meta:
        model = StadionReview
        # fields = "__all__"
        exclude = ('stadion',)


class StadionAddReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadionReview
        fields = ('comment', )
