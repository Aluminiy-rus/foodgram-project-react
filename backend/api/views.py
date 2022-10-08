from django.http.response import HttpResponse
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import ApiPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CustomUserSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    SubscriptionsSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    IngredientSerializer,
    TagSerializer,
)
from recipes.models import (
    Recipe,
    Ingredient,
    Tag,
    Follow,
    Favorite,
    RecipeIngredientAmount,
)
from cart.models import ShoppingCart

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет для юзеров"""

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    pagination_class = ApiPagination
    serializer_class = CustomUserSerializer
    lookup_field = "id"

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        data = {
            "user": user.id,
            "author": author.id,
        }
        serializer = SubscribeSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        queryset = get_object_or_404(Follow, user=user)
        serializer = SubscriptionsSerializer(
            queryset, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        subscribe = get_object_or_404(Follow, user=user, author=author)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        pagination_class=ApiPagination,
    )
    def subscriptions(self, request):
        user = self.request.user
        queryset = Follow.objects.filter(user=user)
        paginated_follow = self.paginate_queryset(queryset=queryset)
        serializer = SubscriptionsSerializer(
            paginated_follow, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(ModelViewSet):
    """Вьюсет для рецептов"""

    permission_classes = [IsAuthorOrReadOnly]
    queryset = Recipe.objects.all()
    pagination_class = ApiPagination
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(
        methods=["post"],
        permission_classes=[IsAuthenticated],
        detail=True,
    )
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            "user": user.id,
            "favorite": recipe.id,
        }
        serializer = FavoriteSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(Favorite, user=user, favorite=recipe)
        favorite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)

        data = {
            "user": user.id,
            "recipe": recipe.id,
        }
        serializer = ShoppingCartSerializer(
            data=data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorites = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
        favorites.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        shopping_cart = user.cart_user.all()
        filename = f"{user.username}_shopping_cart.txt"
        ingredients_list = {}
        for recipes_list in shopping_cart:
            recipe = recipes_list.recipe
            ingredients = RecipeIngredientAmount.objects.filter(recipe=recipe)
            for i in ingredients:
                amount = i.amount
                name = i.ingredient.name
                measurement_unit = i.ingredient.measurement_unit
                if name not in ingredients_list:
                    ingredients_list[name] = {
                        "measurement_unit": measurement_unit,
                        "amount": amount,
                    }
                else:
                    ingredients_list[name]["amount"] = (
                        ingredients_list[name]["amount"] + amount
                    )

        shopping_list = []
        for i in ingredients_list:
            shopping_list.append(
                f'{i} - {ingredients_list[i]["amount"]} '
                f'{ingredients_list[i]["measurement_unit"]} \n'
            )

        response = HttpResponse(
            shopping_list, content_type="text.txt; charset=utf-8"
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов"""

    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ["^name"]


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тэгов"""

    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None
    serializer_class = TagSerializer
