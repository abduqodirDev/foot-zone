from django.urls import path

from useradmin.views import ListStadionAdminAPIView, ListCommonUserAPIView

urlpatterns = [
    path('stadion-admins/', ListStadionAdminAPIView.as_view(), name='stadion-admins'),
    path('common-users/', ListCommonUserAPIView.as_view(), name='common-users'),
]
