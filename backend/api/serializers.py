from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    SlugRelatedField,
    CurrentUserDefault,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    ValidationError,
)
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from .validators import (
    UserNotAuthorValidator,
    UsernameAllowedValidator,
    RecipeIngredientsAmountValidator,
)
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


class ShoppingCartSerializer(ModelSerializer):
    """Сериализатор для списка покупок"""

    class Meta:
        model = ShoppingCart
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
            'id',
            'name',
            'measurement_unit',
            'amount',
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

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, favorite=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=request.user, recipe=obj).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_set = set()
        for ingredient in ingredients:
            if int(ingredient.get('amount')) <= 0:
                raise ValidationError('Кол-во ингредиентов должно быть больше 0')
            id = ingredient.get('id')
            if id in ingredients_set:
                raise ValidationError('Не должено быть повторений.')
            ingredients_set.add(id)
        data['ingredients'] = ingredients
        return data

    def create(self, validated_data):
        image = validated_data.pop("image")
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags = self.initial_data.get("tags")

        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))

        for ingredient in ingredients:
            RecipeIngredientAmount.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )

        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        tags = self.initial_data.get('tags')

        for tag_id in tags:
            instance.tags.add(get_object_or_404(Tag, pk=tag_id))

        RecipeIngredientAmount.objects.filter(recipe=instance).delete()
        for ingredient in validated_data.get('ingredients'):
            ingredients_amounts = RecipeIngredientAmount.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredients_amounts.save()

        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
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

        return RecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class FavoriteSerializer(ModelSerializer):
    """Сериализатор для избранного"""
    favorite = PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=["user", "favorite"],
                message="Уже добалено в избранное.",
            ),
        ]
        fields = ('user', 'favorite')

    def validate(self, data):
        request = self.context.get('request')
        favorite_id = data['favorite'].id
        favorite_exists = Favorite.objects.filter(
            user=request.user,
            favorite__id=favorite_id
        ).exists()

        if request.method == 'GET' and favorite_exists:
            raise ValidationError('Вы уже добавили этот рецепт в избранное')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return SubscriptionsSerializer(instance.favorite, context=context).data
