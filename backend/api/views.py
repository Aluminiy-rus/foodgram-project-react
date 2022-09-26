from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .mixins import GetPostDelMixin, PostDelMixin
from .pagination import ApiPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    RecipeSerializer,
    CustomUserSerializer,
    FavouriteSerializer,
    IngredientSerializer,
    ShoppingCartSerializer,
    FollowSerializer,
    TagSerializer,
)
from recipes.models import Recipe, Ingredient, Tag

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет для пользователей"""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer
    pagination_class = ApiPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username"]
    lookup_field = "username"


class RecipeViewSet(viewsets.ModelViewSet):
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


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тэгов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
