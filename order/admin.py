from django.contrib import admin

from order.models import BronStadion


@admin.register(BronStadion)
class AdminBronStadion(admin.ModelAdmin):
    list_display = ('id', 'stadion', 'user', 'time', 'date', 'is_active')
    list_filter = ('stadion', 'user', 'is_active')
