from django.urls import path

from order.views import BronStadionAPIView, MyBronStadion, MyStadionBronListAPIView


app_name = "order"
urlpatterns = [
    path("stadion/<int:id>/", BronStadionAPIView.as_view(), name="order"),
    path("my-bron/", MyBronStadion.as_view(), name="my-bron"),
    path("my-stadion-bron/", MyStadionBronListAPIView.as_view(), name="my-stadion-bron"),
]
