from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    SlugRelatedField,
    CurrentUserDefault,
    PrimaryKeyRelatedField,
    ReadOnlyField,
)
from rest_framework.validators import (
    UniqueTogetherValidator,
)

from .validators import UserNotAuthorValidator, UsernameAllowedValidator
from recipes.models import (
    Favorite,
    Follow,
    Ingredient,
    Recipe,
    Tag,
    RecipeIngredientAmount,
)
from cart.models import ShoppingCart
from .utils import Base64ImageField, Hex2NameColor

User = get_user_model()


class CustomUserSerializer(ModelSerializer):
    """Сериализатор для юзеров"""

    is_subscribed = SerializerMethodField()

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
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj.id).exists()


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


class RecipeIngredientAmountSerializer(ModelSerializer):
    """Сериализатор для ингредиентов рецепта"""

    id = ReadOnlyField(source="ingredient.id")
    name = ReadOnlyField(source="ingredient.name")
    measurement_unit = ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        model = RecipeIngredientAmount
        fields = "__all__"


class ShoppingCartSerializer(ModelSerializer):
    """Сериализатор для списка покупок"""

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()
    ingredients = RecipeIngredientAmountSerializer(
        source="ingredients_amounts",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
            "is_favorited" "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
            "id",
            "ingredients",
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()


# class SubscriptionRecipeSerializer(ModelSerializer):
#     class Meta:
#         fields = (
#             "id",
#             "name",
#             "image",
#             "cooking_time",
#         )
#         model = Recipe


class SubscribeSerializer(ModelSerializer):
    """Сериализатор для создания и удаления подписок"""

    queryset = User.objects.all()
    user = PrimaryKeyRelatedField(queryset=queryset)
    author = PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=["user", "author"],
            ),
            UserNotAuthorValidator(
                user="user",
                author="author",
            ),
        ]
        fields = (
            "user",
            "author",
        )


class SubscriptionsSerializer(ModelSerializer):
    """Сериализатор для подписок"""

    email = ReadOnlyField(source="author.email")
    id = ReadOnlyField(source="author.id")
    username = ReadOnlyField(source="author.username")
    first_name = ReadOnlyField(source="author.first_name")
    last_name = ReadOnlyField(source="author.last_name")
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        queryset = Recipe.objects.filter(author=obj.author)
        if limit is not None:
            queryset = Recipe.objects.filter(author=obj.author)[: int(limit)]

        return SubscriptionsSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class FavoriteSerializer(ModelSerializer):
    """Сериализатор для избранного"""

    user = SlugRelatedField(
        slug_field="username",
        default=CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    favorite = SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=["user", "favorite"],
            ),
        ]
        fields = "__all__"
