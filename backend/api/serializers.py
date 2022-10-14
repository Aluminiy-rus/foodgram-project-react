from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)
from rest_framework.validators import UniqueTogetherValidator

from .utils import Base64ImageField, Hex2NameColor
from .validators import (
    RecipeIngredientsAmountValidator,
    RecipeIngredientsValidator,
    UsernameAllowedValidator,
    UserNotAuthorValidator,
)
from cart.models import ShoppingCart
from recipes.models import (
    Favorite,
    Follow,
    Ingredient,
    Recipe,
    RecipeIngredientAmount,
    RecipeTag,
    Tag,
)

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
        """Проверка статуса подписки"""
        user = self.context["request"].user
        return user.is_authenticated and user.follow_user.filter(author=obj).exists()


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

    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source="ingredient.id"
    )
    name = CharField(
        source="ingredient.name",
        read_only=True,
    )
    measurement_unit = CharField(
        source="ingredient.measurement_unit",
        read_only=True,
    )

    class Meta:
        model = RecipeIngredientAmount
        validators = [
            RecipeIngredientsAmountValidator(amount="amount"),
        ]
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов"""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()
    text = CharField()
    cooking_time = IntegerField()
    ingredients = RecipeIngredientAmountSerializer(
        source="recipe_ingredient_amount",
        many=True,
    )

    class Meta:
        model = Recipe
        validators = [
            RecipeIngredientsValidator(ingredients="ingredients"),
        ]
        fields = (
            "tags",
            "author",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
            "id",
            "ingredients",
        )

    def _check_fields(self, model, obj):
        user = self.context["request"].user
        return (
            user.is_authenticated
            and model.objects.filter(user=user, recipe=obj).exists()
        )

    def get_is_favorited(self, obj):
        return self._check_fields(Favorite, obj)

    def get_is_in_shopping_cart(self, obj):
        return self._check_fields(ShoppingCart, obj)

    def _create_or_update(self, recipe, data_ingredients):
        tags_objs = [
            RecipeTag(recipe=recipe, tag=Tag.objects.get(id=tag))
            for tag in data_ingredients.data["tags"]
        ]
        RecipeTag.objects.bulk_create(tags_objs)

        ingr_objs = [
            RecipeIngredientAmount(
                recipe=recipe,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )
            for ingredient in data_ingredients.data["ingredients"]
        ]
        RecipeIngredientAmount.objects.bulk_create(ingr_objs)
        return recipe

    def create(self, validated_data):
        context = self.context["request"]
        validated_data.pop("recipe_ingredient_amount")
        recipe = Recipe.objects.create(**validated_data)
        return self._create_or_update(recipe=recipe, data_ingredients=context)

    def update(self, instance, validated_data):
        context = self.context["request"]
        validated_data.pop("recipe_ingredient_amount")
        super().update(validated_data=validated_data, instance=instance)
        RecipeIngredientAmount.objects.filter(recipe=instance).delete()
        RecipeTag.objects.filter(recipe=instance).delete()
        return self._create_or_update(recipe=instance, data_ingredients=context)

    def to_representation(self, instance):
        response = super(RecipeSerializer, self).to_representation(instance)
        return response


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


class RepresentationRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class SubscriptionsSerializer(CustomUserSerializer):
    """Сериализатор для подписок"""

    recipes = RepresentationRecipeSerializer(many=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
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

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
