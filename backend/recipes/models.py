from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

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
        max_length=7,
        validators=[
            RegexValidator(
                regex=r"^[A-Fa-f0-9]{6}$",
                message="Значение цвета необходимо указывать в формате HEX-кода!",
            ),
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
        unique=True,
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
        blank=True,
    )
    text = models.CharField(
        verbose_name="Описание",
        null=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredientValue",
        on_delete=models.PROTECT,
        null=False,
        related_name="ingridients",
        verbose_name="Ингредиенты рецепта",
        db_index=True,
        help_text="Необходимые ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        on_delete=models.PROTECT,
        related_name="tags",
        db_index=True,
    )
    сooking_time = models.TimeField(
        verbose_name="Время приготовления",
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


class RecipeIngredientValue(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, verbose_name="Ингредиент"
    )
    value = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                limit_value=0,
                message="Минимальное значение должно быть больше 0",
            ),
        ],
        verbose_name="Количество",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="recipe_ingredient_value",
                fields=["recipe", "ingredient", "value"],
            ),
        ]


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.PROTECT,
        verbose_name="Тэг",
    )


class Follow(models.Model):
    """Модель подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор рецепта",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_follow",
            )
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Favourite(models.Model):
    """Модель избранного"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Подписчик",
    )
    favourite = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favourite",
        verbose_name="Избранный рецепт",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "favourite"], name="unique_favourites"
            )
        ]
        verbose_name = "Избранное"
