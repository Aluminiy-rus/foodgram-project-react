from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from .validators import UsernameNotMeValidator
from recipes.models import (
    Favourite,
    Follow,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        validators = [
            UsernameNotMeValidator(
                username="username",
            ),
        ]
        fields = ("username", "email")


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=["username", "email"],
            ),
        ]
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ["role"]
