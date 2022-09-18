from rest_framework import serializers
from rest_framework.validators import (
    UniqueTogetherValidator,
)

from .validators import UsernameAllowedValidator, UserNotAuthorValidator
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
            UsernameAllowedValidator(
                username="username",
            ),
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=["username", "email"],
            ),
        ]
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )


class TokenSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
    )
    email = serializers.CharField(
        required=True,
    )

    class Meta:
        fields = ("auth_token",)


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
        )


class UserSetPasswordSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "new_password",
            "current_password",
        )


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=["user", "following"],
            ),
            UserNotAuthorValidator(
                user="user",
                following="following",
            ),
        ]
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = "__all__"


class FavouriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    favourite = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Favourite
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=["user", "favourite"],
            ),
        ]
        fields = "__all__"


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = "__all__"
