from django.urls import path

from common.views import LikedStadionView, StartsPostAPIView, DeleteLikedStadionView


app_name = 'common'
urlpatterns = [
    path('liked-stadion/', LikedStadionView.as_view(), name='liked-stadion'),
    path('delete-liked-stadion/<int:id>/', DeleteLikedStadionView.as_view(), name='delete-liked-stadion'),
    path('rank-stadion/', StartsPostAPIView.as_view(), name='rank-stadion'),
]
