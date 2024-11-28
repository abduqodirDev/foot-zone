from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import User, VerificationOtp


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number", "email", "middle_name", "date_of_birth", "sex", "role", "photo")}),
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
                "fields": ("username", "usable_password", "role", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "first_name", "last_name", "role", "is_staff")

admin.site.unregister(Group)


@admin.register(VerificationOtp)
class AdminVerifyOTP(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'is_confirmed')
    list_filter = ('user', 'is_confirmed')
    search_fields = ('user', 'code')
