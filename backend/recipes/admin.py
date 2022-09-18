from django.contrib import admin

from .models import Favourite, Follow, Ingredient, Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )
    search_fields = (
        "name",
        "slug",
    )
    list_filter = (
        "name",
        "slug",
    )
    empty_value_field = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "units",
    )
    search_fields = (
        "name",
        "units",
    )
    list_filter = (
        "name",
        "units",
    )
    empty_value_field = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "ingredients",
        "tags",
        "pub_date",
    )
    search_fields = (
        "name",
        "author",
        "ingredients",
        "tags",
        "pub_date",
    )
    list_filter = (
        "name",
        "author",
        "ingredients",
        "tags",
        "pub_date",
    )
    empty_value_field = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )
    search_fields = (
        "user",
        "author",
    )
    list_filter = (
        "user",
        "author",
    )
    empty_value_field = "-пусто-"


class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "favourite",
    )
    search_fields = (
        "user",
        "favourite",
    )
    list_filter = (
        "user",
        "favourite",
    )
    empty_value_field = "-пусто-"


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favourite, FavouriteAdmin)
