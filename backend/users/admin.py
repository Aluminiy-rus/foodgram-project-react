from django.contrib import admin

from .models import User


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
    )
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
    )
    list_filter = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
    )
    empty_value_field = "-пусто-"


admin.site.register(User, UsersAdmin)
