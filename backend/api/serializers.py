from wsgiref.validate import validator

from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    SerializerMethodField,
    ValidationError,
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
        user = self.context["request"].user
        return (
            user.is_authenticated
            and user.follow_user.filter(author=obj).exists()
        )


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
        validators = [
            UniqueTogetherValidator(
                queryset=RecipeIngredientAmount.objects.all(),
                fields=["recipe", "ingredient", "amount"],
                message="Не уникальное сочетание - рецепт/ингредиент/кол-во.",
            ),
            RecipeIngredientsAmountValidator(amount="amount"),
        ]
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()
    ingredients = RecipeIngredientAmountSerializer(
        source="recipe_ingredient_amount",
        many=True,
        read_only=True,
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

    # def validate(self, data):
    #     ingredients = self.initial_data.get("ingredients")
    #     ingredients_set = set()
    #     for ingredient in ingredients:
    #         if int(ingredient.get("amount")) <= 0:
    #             raise ValidationError("Кол-во должно быть больше 0")
    #         pk = ingredient.get("id")
    #         if pk in ingredients_set:
    #             raise ValidationError("Не должено быть повторений.")
    #         ingredients_set.add(pk)
    #     data["ingredients"] = ingredients
    #     return data

    def create(self, validated_data):
        tags = self.initial_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)

        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))

        # for ingredient in ingredients:
        #     RecipeIngredientAmount.objects.create(
        #         recipe=recipe,
        #         ingredient_id=ingredient.get("id"),
        #         amount=ingredient.get("amount"),
        #     )

        for ingredient in ingredients:
            ingredient = RecipeIngredientAmount.objects.bulk_create(
                RecipeIngredientAmount(
                    recipe=recipe,
                    ingredient_id=ingredient.get("id"),
                    amount=ingredient.get("amount"),
                )
            )

        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        tags = self.initial_data.get("tags")

        for tag_id in tags:
            instance.tags.add(get_object_or_404(Tag, pk=tag_id))

        RecipeIngredientAmount.objects.filter(recipe=instance).delete()
        for ingredient in validated_data.get("ingredients"):
            ingredients_amounts = RecipeIngredientAmount.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )
            ingredients_amounts.save()

        if validated_data.get("image") is not None:
            instance.image = validated_data.get("image")
        instance.name = validated_data.get("name")
        instance.text = validated_data.get("text")
        instance.cooking_time = validated_data.get("cooking_time")
        instance.save()

        return instance


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


class SubscriptionsSerializer(ModelSerializer):
    """Сериализатор для подписок"""

    is_subscribed = SerializerMethodField()
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

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return (
            user.is_authenticated
            and user.follow_user.filter(author=obj).exists()
        )

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
