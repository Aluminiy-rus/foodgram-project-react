from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SlugRelatedField,
    CurrentUserDefault,
)
from rest_framework.validators import (
    UniqueTogetherValidator,
)

from .validators import UserNotAuthorValidator, UsernameAllowedValidator
from recipes.models import (
    Favourite,
    Follow,
    Ingredient,
    Recipe,
    Tag,
)
from cart.models import ShoppingCart
from .utils import Base64ImageField, Hex2NameColor

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        validators = [
            UsernameAllowedValidator(
                username="username",
            ),
        ]
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            # "is_subscribed",
        )


class FollowSerializer(ModelSerializer):
    """Сериализатор для подписок"""

    user = SlugRelatedField(
        slug_field="username",
        default=CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    following = SlugRelatedField(
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


class TagSerializer(ModelSerializer):
    """Сериализатор для тэгов"""

    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингредиентов"""

    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов"""

    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    name = CharField(source="name")
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = "__all__"


class FavouriteSerializer(ModelSerializer):
    """Сериализатор для избранного"""

    user = SlugRelatedField(
        slug_field="username",
        default=CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    favourite = SlugRelatedField(
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


class ShoppingCartSerializer(ModelSerializer):
    """Сериализатор для списка покупок"""

    class Meta:
        model = ShoppingCart
        fields = "__all__"
