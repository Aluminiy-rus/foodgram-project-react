from django.contrib.admin import ModelAdmin, site, TabularInline

from .models import (
    Favorite,
    Follow,
    Ingredient,
    Recipe,
    Tag,
    RecipeTag,
    RecipeIngredientAmount,
)


class RecipeIngredientAmountInLine(TabularInline):
    model = RecipeIngredientAmount
    verbose_name = "Ингредиент рецепта"
    verbose_name_plural = "Ингредиенты рецепта"
    extra = 1


class RecipeTagInLine(TabularInline):
    model = RecipeTag
    verbose_name = "Тег рецепта"
    verbose_name_plural = "Теги рецепта"
    extra = 1


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
    inlines = (
        RecipeIngredientAmountInLine,
        RecipeTagInLine,
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


class FavoriteAdmin(ModelAdmin):
    list_display = (
        "user",
        "favorite",
    )
    search_fields = (
        "user",
        "favorite",
    )
    list_filter = (
        "user",
        "favorite",
    )
    empty_value_field = "-пусто-"


site.register(Tag, TagAdmin)
site.register(Ingredient, IngredientAdmin)
site.register(Recipe, RecipeAdmin)
site.register(Follow, FollowAdmin)
site.register(Favorite, FavoriteAdmin)
