from django.contrib.admin import ModelAdmin, site

from .models import Favourite, Follow, Ingredient, Recipe, Tag


class TagAdmin(ModelAdmin):
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


class IngredientAdmin(ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = (
        "name",
        "measurement_unit",
    )
    list_filter = (
        "name",
        "measurement_unit",
    )
    empty_value_field = "-пусто-"


class RecipeAdmin(ModelAdmin):
    list_display = (
        "name",
        "author",
        "pub_date",
    )
    search_fields = (
        "name",
        "author",
        "pub_date",
    )
    list_filter = (
        "name",
        "author",
        "pub_date",
    )
    empty_value_field = "-пусто-"


class FollowAdmin(ModelAdmin):
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


class FavouriteAdmin(ModelAdmin):
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


site.register(Tag, TagAdmin)
site.register(Ingredient, IngredientAdmin)
site.register(Recipe, RecipeAdmin)
site.register(Follow, FollowAdmin)
site.register(Favourite, FavouriteAdmin)
