from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (
    AllValuesMultipleFilter,
    BooleanFilter,
    ModelChoiceFilter,
)
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ValidationError

from recipes.models import Recipe

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    search_param = "name"


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name="tags__slug")
    author = ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = BooleanFilter(method="get_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = [
            "tags",
            "author",
        ]

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        elif not value and self.request.user.is_authenticated:
            return queryset.exclude(favorite__user=self.request.user)
        else:
            raise ValidationError(
                "Вы не авторизованы для фильтрации по избранному."
            )

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        elif not value and self.request.user.is_authenticated:
            return queryset.exclude(shopping_cart__user=self.request.user)
        else:
            raise ValidationError(
                "Вы не авторизованы для фильтрации по списку покупок."
            )
