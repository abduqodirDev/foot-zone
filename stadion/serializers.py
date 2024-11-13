from rest_framework import serializers

from stadion.models import Stadion, Images


class StadionSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField("comment_count_def")
    rank_ratio = serializers.SerializerMethodField("rank_ratio_def")
    class Meta:
        model = Stadion
        fields = ['id', 'title', 'price', 'latitude', 'longitude', 'photo', 'comment_count', 'rank_ratio']

    def comment_count_def(self, obj):
        return obj.stadionreviews.count()

    def rank_ratio_def(self, obj):
        reviews = obj.stadionreviews.all()
        if not reviews:
            return 0
        sum = 0
        for review in reviews:
            sum += review.rank

        return sum/len(reviews)
