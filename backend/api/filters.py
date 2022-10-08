from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (
    AllValuesMultipleFilter,
    ModelChoiceFilter,
    BooleanFilter,
)
from rest_framework.serializers import ValidationError
from rest_framework.filters import SearchFilter

from recipes.models import (
    Recipe,
)

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
        if value is True and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        elif value is False and self.request.user.is_authenticated:
            return queryset.exclude(favorites__user=self.request.user)
        else:
            raise ValidationError(
                "Вы не авторизованы для фильтрации по избранному."
            )

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value is True and self.request.user.is_authenticated:
            return queryset.filter(cart_recipe__user=self.request.user)
        else:
            raise ValidationError(
                "Вы не авторизованы для фильтрации по списку покупок."
            )
