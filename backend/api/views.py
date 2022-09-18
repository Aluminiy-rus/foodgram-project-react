from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .mixins import GetPostDelMixin, PostDelMixin
from .pagination import ApiPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    RecipeSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSetPasswordSerializer,
    UserSerializer,
    FavouriteSerializer,
    IngredientSerializer,
    ShoppingCartSerializer,
    FollowSerializer,
    TagSerializer,
)
from recipes.models import Recipe, Ingredient, Tag
from users.confirm_code_generator import confirm_code_generator
from users.models import User


class SignUp(APIView):
    """Вью для регистрации"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirm_code_generator(user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class Token(APIView):
    """Вью для токенов"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data["username"]
        )
        confirmation_code = serializer.validated_data["confirmation_code"]
        if confirmation_code == confirm_code_generator(user):
            token = {"token": str(AccessToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей"""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
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
    def user_me(self, request):
        user = self.request.user
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return None

    @action(
        methods=["post"],
        detail=False,
        url_path="set_password",
        permission_classes=[IsAuthenticated],
    )
    def user_set_password(self, request):
        if request.method == "POST":
            user = self.request.user
            serializer = UserSetPasswordSerializer(
                user,
                data=request.data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return None


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
