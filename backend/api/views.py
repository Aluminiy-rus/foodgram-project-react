from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .mixins import GetPostDelMixin
from .pagination import ApiPagination
from .permissions import AuthorOrAdminOrReadOnly, IsAdmin, IsAdminOrReadOnly
from .serializers import (SignUpSerializer, TokenSerializer, UserSerializer, UserMeSerializer)
from recipes.models import Recipe
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
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer
    pagination_class = ApiPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username"]
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def user_me_actions(self, request):
        user = self.request.user
        if request.method == "GET":
            serializer = UserMeSerializer(user)
            return Response(serializer.data)
        if request.method == "PATCH":
            user = self.request.user
            serializer = UserMeSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return None
