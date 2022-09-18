from django.contrib import admin

from .models import ShoppingCart


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "shopping_cart",
    )
    search_fields = (
        "user",
        "shopping_cart",
    )
    list_filter = (
        "user",
        "shopping_cart",
    )
    empty_value_field = "-пусто-"


admin.site.register(ShoppingCart, ShoppingCartAdmin)
