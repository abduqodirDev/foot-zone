from django.contrib import admin
from common.models import LikedStadion


@admin.register(LikedStadion)
class LikedStadionAdmin(admin.ModelAdmin):
    list_filter = ('user', 'stadion')
    search_fields = ('user', 'stadion')
    list_display = ('id', 'user', 'stadion')
