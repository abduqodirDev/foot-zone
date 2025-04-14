from django.urls import path

from stadion.views import (
    StadionListAPIView, DetailStadionAPIView, AddStadionAPIView, AllStadionMapAPIView,
    StadionImageAPIView, StadionReviewAPIView, AdminStadionListAPIView, AdminStadionUpdateAPIView,
    AdminStadionDeleteAPIView, StadionStatistikaKunAPIView, StadionStatistikaOyAPIView, StadionStatistikaYilAPIView,
    StadionStatistikaUmumAPIView, StadionStatistikaKunlarAPIView, StadionEditPriceAPIView, StadionImagesAPIView,
    StadionImagesDeleteAPIView, StadionImagesAllAPIView, StadionTimeActiveAPIView, CreateStadionReviewAPIView,
)

app_name = "stadion"
urlpatterns = [
    path('all-stadion/', StadionListAPIView.as_view(), name='all-stadion'),
    path('all-map/', AllStadionMapAPIView.as_view(), name='all-map'),
    path('<int:id>/', DetailStadionAPIView.as_view(), name='detail-stadion'),
    path('add-stadion/', AddStadionAPIView.as_view(), name='add-stadion'),
    path('stadion-images/', StadionImageAPIView.as_view(), name='stadion-images'),
    path('stadion-review/<int:id>/', StadionReviewAPIView.as_view(), name='stadion-review'),

    path('admin-stadion-get/', AdminStadionListAPIView.as_view(), name='admin-stadion-get'),
    path('admin-stadion-put/<int:id>/', AdminStadionUpdateAPIView.as_view(), name='admin-stadion-put'),
    path('admin-stadion-delete/<int:id>/', AdminStadionDeleteAPIView.as_view(), name='admin-stadion-delete'),

    path('statistika-kun/', StadionStatistikaKunAPIView.as_view(), name='statistika-kun'),
    path('statistika-oy/', StadionStatistikaOyAPIView.as_view(), name='statistika-oy'),
    path('statistika-yil/', StadionStatistikaYilAPIView.as_view(), name='statistika-yil'),
    path('statistika-umum/', StadionStatistikaUmumAPIView.as_view(), name='statistika-umum'),
    path('statistika-kunlar/', StadionStatistikaKunlarAPIView.as_view(), name='statistika-kunlar'),

    path('edit-price/<int:id>/', StadionEditPriceAPIView.as_view(), name='edit-price'),
    path('edit-time-active/<int:id>/', StadionTimeActiveAPIView.as_view(), name='edit-time-active'),

    path('stadion-images/<int:id>/', StadionImagesAPIView.as_view(), name='stadion-images'),
    path('stadion-images/<int:id>/delete/<int:pk>/', StadionImagesDeleteAPIView.as_view(), name='stadion-images-delete'),
    path('stadion-images/all-add/', StadionImagesAllAPIView.as_view(), name='stadion-images-all-add'),

    path('StadionReviewAdd/', CreateStadionReviewAPIView.as_view()),
]
