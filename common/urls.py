from django.urls import path

from common.views import LikedStadionView


app_name = 'common'
urlpatterns = [
    path('liked-stadion/', LikedStadionView.as_view(), name='liked-stadion'),
    # path('stadion-money-statistika/', StadionMoneyStatistika.as_view(), name='stadion-money-statistika'),
]
