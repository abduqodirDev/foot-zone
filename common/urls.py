from django.urls import path

from common.views import LikedStadionView


urlpatterns = [
    path('liked-stadion/', LikedStadionView.as_view, name='liked-stadion'),
]
