from django.urls import path

from order.views import BronStadionAPIView


app_name = "order"
urlpatterns = [
    path("stadion/<int:id>/", BronStadionAPIView.as_view(), name="order"),
]
