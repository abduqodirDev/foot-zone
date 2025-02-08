from django.urls import path
from .views import ViloyatListAPIView

urlpatterns = [
    path('viloyatlar/', ViloyatListAPIView.as_view(), name='viloyatlar'),
]
