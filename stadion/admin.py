from django.contrib import admin

from stadion.models import Stadion, Images, StadionReview, StadionPrice


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1


class PriceInline(admin.TabularInline):
    model = StadionPrice
    extra = 1


@admin.register(Stadion)
class StadionAdmin(admin.ModelAdmin):
    inlines = [ImagesInline, PriceInline]
    list_display = ['title', 'user', 'photo']
    list_filter = ['user']
    search_fields = ['title']


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'stadion', 'image', 'image_tag']
    readonly_fields = ('image_tag',)


@admin.register(StadionPrice)
class StadionPriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'stadion', 'time', 'price']
    list_filter = ['stadion']


@admin.register(StadionReview)
class StadionReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'stadion', 'user', 'created_at']
    list_filter = ['stadion', 'user']
