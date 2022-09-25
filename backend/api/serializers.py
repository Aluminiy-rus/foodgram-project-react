from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    SlugRelatedField,
    CurrentUserDefault,
)
from rest_framework.validators import (
    UniqueTogetherValidator,
)

from .validators import UsernameAllowedValidator, UserNotAuthorValidator
from recipes.models import (
    Favourite,
    Follow,
    Ingredient,
    Recipe,
    Tag,
)
from cart.models import ShoppingCart
from users.models import User
from .utils import Base64ImageField, Hex2NameColor


# class SignUpSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         validators = [
#             UsernameAllowedValidator(
#                 username="username",
#             ),
#             UniqueTogetherValidator(
#                 queryset=User.objects.all(),
#                 fields=["username", "email"],
#             ),
#         ]
#         fields = (
#             "username",
#             "email",
#             "first_name",
#             "last_name",
#         )


class TokenSerializer(Serializer):
    password = CharField(
        required=True,
    )
    email = CharField(
        required=True,
    )

    class Meta:
        fields = ("auth_token",)


class UserSerializer(ModelSerializer):
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


class FollowSerializer(ModelSerializer):
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
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(ModelSerializer):
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
    class Meta:
        model = ShoppingCart
        fields = "__all__"
