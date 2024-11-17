class StadionReviewMixin:
    def comment_count_def(self, obj):
        return obj.stadionreviews.count()

    def rank_ratio_def(self, obj):
        reviews = obj.stadionreviews.all()
        if not reviews:
            return 0
        sum = 0
        for review in reviews:
            sum += review.rank
        return sum / len(reviews)
