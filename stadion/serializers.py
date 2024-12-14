from rest_framework import serializers

from stadion.models import Stadion, Images, StadionReview
from stadion.mixings import StadionReviewMixin
from users.models import User


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('id', 'image')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadionReview
        fields = ('user', 'comment', 'rank', 'created_at')


class StadionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number')


class StadionSerializer(serializers.ModelSerializer, StadionReviewMixin):
    comment_count = serializers.SerializerMethodField("get_comment_count")
    rank_ratio = serializers.SerializerMethodField("get_rank_ratio")
    class Meta:
        model = Stadion
        fields = ['id', 'title', 'address', 'price', 'photo', 'comment_count', 'rank_ratio']

    def get_comment_count(self, obj):
        return self.comment_count_def(obj)

    def get_rank_ratio(self, obj):
        return self.rank_ratio_def(obj)


class StadionDetailSerializer(serializers.ModelSerializer, StadionReviewMixin):
    user = StadionUserSerializer()
    comment_count = serializers.SerializerMethodField("get_comment_count")
    rank_ratio = serializers.SerializerMethodField("get_rank_ratio")
    class Meta:
        model = Stadion
        fields = "__all__"

    def get_comment_count(self, obj):
        return self.comment_count_def(obj)

    def get_rank_ratio(self, obj):
        return self.rank_ratio_def(obj)

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
