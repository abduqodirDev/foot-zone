from django.urls import path

from stadion.views import StadionListAPIView

app_name="stadion"
urlpatterns = [
    path('all-stadion/', StadionListAPIView.as_view(), name='all-stadion'),
]
