from django.contrib import admin

from stadion.models import Stadion, Images, StadionReview


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1


@admin.register(Stadion)
class StadionAdmin(admin.ModelAdmin):
    inlines = [ImagesInline,]
    list_display = ['title', 'price', 'user', 'start_time', 'end_time', 'photo']
    list_filter = ['price', 'user']
    search_fields = ['title']


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'stadion', 'image', 'image_tag']
    readonly_fields = ('image_tag',)


@admin.register(StadionReview)
class StadionReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'stadion', 'user', 'rank', 'created_at']
    list_filter = ['stadion', 'user', 'rank']
