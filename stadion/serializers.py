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
    star = serializers.FloatField(source='star_avg', read_only=True)
    # star = serializers.SerializerMethodField("get_star")
    viloyat = serializers.StringRelatedField()
    tuman = serializers.StringRelatedField()
    class Meta:
        model = Stadion
        fields = ['id', 'title', 'price', 'address', 'photo', 'star', 'viloyat', 'tuman']

    # def get_star(self, obj):
    #     count = 0
    #     starts = obj.StadionStarts.all()
    #     if len(starts) == 0:
    #         return 0
    #     for star in starts:
    #         count += star.rank
    #     return round(count / len(starts), 2)


class StadionDetailSerializer(serializers.ModelSerializer):
    user = StadionUserSerializer()
    star = serializers.SerializerMethodField("get_star")
    viloyat = serializers.StringRelatedField()
    tuman = serializers.StringRelatedField()
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
        return str(round(count / len(starts),1))


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


class AllStadionMapSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


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
        exclude = ('stadion',)


class StadionAddReviewSerializer(serializers.Serializer):
    comment = serializers.CharField()


class StadionEditPriceSerializer(serializers.Serializer):
    time = serializers.IntegerField(required=True, min_value=0, max_value=23)
    price = serializers.IntegerField(required=True, min_value=0)


class StadionImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('id', 'image')


class StadionImagesAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('image', )


class StadionImageUploadSerializer(serializers.Serializer):
    stadion_id = serializers.IntegerField()
    images = serializers.ListField(child=serializers.ImageField(), max_length=5)

    def validate(self, data):
        stadion = Stadion.objects.get(id=data["stadion_id"])
        if stadion.images.count() + len(data["images"]) > 5:
            raise serializers.ValidationError("5 tadan ortiq rasm qo‘sha olmaysiz")
        return data

    def create(self, validated_data):
        stadion = Stadion.objects.get(id=validated_data["stadion_id"])
        images = validated_data["images"]

        stadion_images = [Images(stadion=stadion, image=image) for image in images]
        Images.objects.bulk_create(stadion_images)

        return stadion_images

