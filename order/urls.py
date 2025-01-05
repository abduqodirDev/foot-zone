from django.urls import path

from order.views import BronStadionAPIView, MyBronStadion, MyStadionBronListAPIView, VerifyBronAPIView, \
    StadionBronDiagrammaAPIView, MyStadionHistoryBronAPIView

app_name = "order"
urlpatterns = [
    path("stadion/<int:id>/", BronStadionAPIView.as_view(), name="order"),

    path("my-bron/", MyBronStadion.as_view(), name="my-bron"),
    path("my-stadion-bron/", MyStadionBronListAPIView.as_view(), name="my-stadion-bron"),
    path("my-stadion-history-bron/", MyStadionHistoryBronAPIView.as_view(), name="my-stadion-history-bron"),
    path("verify-stadion-bron/", VerifyBronAPIView.as_view(), name="verify-stadion-bron"),
    path("stadion-statistika/<int:id>/", StadionBronDiagrammaAPIView.as_view(), name="stadion-statistika"),
]
