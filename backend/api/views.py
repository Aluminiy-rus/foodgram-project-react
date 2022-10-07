from django.db.models import Exists, OuterRef
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

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
from recipes.models import Recipe, Ingredient, Tag, Follow, Favorite
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
        serializer = SubscribeSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        queryset = get_object_or_404(Follow, user=user)
        serializer = SubscriptionsSerializer(queryset, context={"request": request})

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

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Recipe.objects.all()
        queryset = Recipe.objects.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(user=user, favorite_id=OuterRef("id"))
            ),
            is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(user=user, favorite_id=OuterRef("id"))
            ),
        )
        if self.request.GET.get("is_favorited"):
            return queryset.filter(is_favorited=True)
        elif self.request.GET.get("is_in_shopping_cart"):
            return queryset.filter(is_in_shopping_cart=True)
        return queryset

    @action(
        methods=['post'],
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
        serializer = FavoriteSerializer(data=data, context={"request": request})
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


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов"""

    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тэгов"""

    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None
    serializer_class = TagSerializer
