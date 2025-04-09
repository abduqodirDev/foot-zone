from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import User, VerificationOtp, PhoneNumber


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "role", "photo")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "usable_password", "role", "password1", "password2"),
            },
        ),
    )
    list_display = ("phone_number", "first_name", "last_name", "role", "is_staff", "is_active")
    ordering = ("phone_number",)

admin.site.unregister(Group)


@admin.register(VerificationOtp)
class AdminVerifyOTP(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'is_confirmed')
    list_filter = ('user', 'is_confirmed')
    search_fields = ('user', 'code')


@admin.register(PhoneNumber)
class PhoneNumber(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'user', 'is_active')
    list_filter = ('user', 'is_active')
