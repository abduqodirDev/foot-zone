from django.contrib import admin

from utils.models import Viloyat, Tuman


@admin.register(Viloyat)
class ViloyatAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tuman)
class TumanAdmin(admin.ModelAdmin):
    list_display = ('name', 'viloyat')
    list_filter = ('viloyat',)
