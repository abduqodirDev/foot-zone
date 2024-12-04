from django.urls import path

from stadion.views import StadionListAPIView, DetailStadionAPIView, AddStadionAPIView

app_name="stadion"
urlpatterns = [
    path('all-stadion/', StadionListAPIView.as_view(), name='all-stadion'),
    path('<int:id>/', DetailStadionAPIView.as_view(), name='detail-stadion'),
    path('add-stadion/', AddStadionAPIView.as_view(), name='add-stadion'),
]
