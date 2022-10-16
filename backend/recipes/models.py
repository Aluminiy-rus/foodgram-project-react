from django.db import models

from .validators import HexColorValidator
from users.models import User


class Tag(models.Model):
    """Модель тегов"""

    name = models.CharField(
        max_length=200,
        verbose_name="Тег",
        unique=True,
        db_index=True,
    )
    color = models.CharField(
        max_length=16,
        validators=[
            HexColorValidator(),
        ],
        default="#ffffff",
        help_text="Цвет в формате HEX-кода (например, #49B64E).",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиентов"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
        unique=True,
        db_index=True,
    )
    measurement_unit = models.CharField(
        max_length=24,
        verbose_name="Еденица измерения",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="recipes",
        db_index=True,
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
        unique=True,
        db_index=True,
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="recipes/images/",
    )
    text = models.TextField(
        verbose_name="Описание",
        null=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredientAmount",
        related_name="recipes",
        verbose_name="Ингредиенты рецепта",
        db_index=True,
        help_text="Необходимые ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        through="RecipeTag",
        related_name="recipes",
        db_index=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        null=False,
        blank=False,
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="author_recipe_unique",
                fields=["author", "name"],
            ),
        ]
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class RecipeIngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredient_amount",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name="recipe_ingredient_amount",
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        null=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_recipe_ingredient_amount",
                fields=["recipe", "ingredient"],
            ),
        ]


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="RecipeTag",
        verbose_name="Рецепт",
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.PROTECT,
        related_name="RecipeTag",
        verbose_name="Тэг",
    )


class Follow(models.Model):
    """Модель подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follow_user",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follow_author",
        verbose_name="Автор рецепта",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_follow",
            )
        ]
        ordering = ["author"]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Favorite(models.Model):
    """Модель избранного"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Подписчик",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Избранный рецепт",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_favorites",
            )
        ]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
