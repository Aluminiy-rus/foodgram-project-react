from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import UserSerializer
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .mixins import GetPostDelMixin, PostDelMixin
from .pagination import ApiPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CustomUserSerializer,
    # SubscriptionUserSerializer,
    RecipeSerializer,
    FavouriteSerializer,
    IngredientSerializer,
    ShoppingCartSerializer,
    FollowSerializer,
    TagSerializer,
)
from recipes.models import Recipe, Ingredient, Tag, Follow

User = get_user_model()


class CustomUserViewSet(ModelViewSet):
    """Вьюсет для пользователей"""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer
    pagination_class = ApiPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username"]
    lookup_field = "username"

    @action(
        methods=["get"],
        detail=False,
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def user_me_actions(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # @action(
    #     methods=['get'],
    #     detail=False,
    #     url_path="subscriptions",
    #     permission_classes=[IsAuthenticated],
    # )
    # def subscriptions(self, request):
    #     user = self.request.user
    #     is_subscribed = Follow.objects.filter(user=user).all()


class RecipeViewSet(ModelViewSet):
    """Вьюсет для рецептов"""

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = RecipeSerializer
    pagination_class = ApiPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavouriteViewSet(PostDelMixin):
    """Вьюсет для избранного"""

    permission_classes = [IsAuthenticated]
    serializer_class = FavouriteSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("favourite__username",)

    def get_queryset(self):
        user = self.request.user
        return user.favourite.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, serializer):
        serializer.save(user=self.request.user)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class ShoppingCartViewSet(GetPostDelMixin):
    """Вьюсет для списка покупок"""

    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingCartSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("shopping_cart__username",)

    def get_queryset(self):
        user = self.request.user
        return user.shopping_cart.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(GetPostDelMixin):
    """Вьюсет для подписок"""

    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("author__username",)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тэгов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
