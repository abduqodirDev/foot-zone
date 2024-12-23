from django.urls import path

from common.views import LikedStadionView, StartsPostAPIView


app_name = 'common'
urlpatterns = [
    path('liked-stadion/', LikedStadionView.as_view(), name='liked-stadion'),
    path('rank-stadion/', StartsPostAPIView.as_view(), name='rank-stadion'),
]
