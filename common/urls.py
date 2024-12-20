from django.urls import path

from common.views import LikedStadionView, LikedStadionPostDeleteView


app_name = 'common'
urlpatterns = [
    path('liked-stadion/', LikedStadionView.as_view(), name='liked-stadion'),
    path('liked-stadion-post-delete/<int:id>/', LikedStadionPostDeleteView.as_view(), name='liked-stadion-post-delete'),
]
