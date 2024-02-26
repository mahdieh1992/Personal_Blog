from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()


class ProfileInLine(admin.TabularInline):
    model = Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_confirm",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("expire_date", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = ("id", "email", "is_staff", "expire_date", "is_confirm")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_confirm")
    search_fields = (
        "email",
        "mobile",
    )
    ordering = ("is_active",)
    inlines = (ProfileInLine,)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "show_image",
        "first_name",
        "last_name",
        "national_code",
    )
