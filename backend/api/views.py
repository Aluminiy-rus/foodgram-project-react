from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import ApiPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CustomUserSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RepresentationRecipeSerializer,
    SubscribeSerializer,
    SubscriptionsSerializer,
    TagSerializer,
)
from cart.models import ShoppingCart
from recipes.models import (
    Favorite,
    Follow,
    Ingredient,
    Recipe,
    RecipeIngredientAmount,
    Tag,
)

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
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, *args, **kwargs):
        user = self.request.user
        author = self.get_object()
        if request.method == "POST":
            data = {
                "user": user.id,
                "author": author.id,
            }
            serializer = SubscribeSerializer(
                data=data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = SubscriptionsSerializer(
                author, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
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
        queryset = User.objects.filter(follow_author__user=user)
        paginated_follow = self.paginate_queryset(queryset=queryset)
        serializer = SubscriptionsSerializer(
            paginated_follow, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(ModelViewSet):
    """Вьюсет для рецептов"""

    permission_classes = [IsAuthorOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = ApiPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def _do_post_delete(self, request, model):
        user = self.request.user
        recipe = self.get_object()
        if request.method == "POST":
            if model.objects.filter(
                user=user,
                recipe=recipe,
            ).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            model.objects.create(
                user=user,
                recipe=recipe,
            )
            serializer = RepresentationRecipeSerializer(
                recipe,
                context={"request": request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            item = get_object_or_404(model, user=user, recipe=recipe)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
        detail=True,
    )
    def favorite(self, request, pk=None):
        return self._do_post_delete(request, Favorite)

    @action(
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
        detail=True,
    )
    def shopping_cart(self, request, pk=None):
        return self._do_post_delete(request, ShoppingCart)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        filename = f"{user.username}_shopping_cart.txt"

        ingredients = (
            RecipeIngredientAmount.objects.filter(
                recipe__shopping_cart__user=user
            )
            .values(
                ingr_name=F("ingredient__name"),
                unit=F("ingredient__measurement_unit"),
            )
            .annotate(amount_sum=Sum("amount"))
        )
        shopping_list = list()
        for ingr in ingredients:
            shopping_list += (
                f'{ingr["ingr_name"]}: {ingr["amount_sum"]} {ingr["unit"]}\n'
            )

        response = HttpResponse(
            shopping_list, content_type="text/plain; charset=utf-8"
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
