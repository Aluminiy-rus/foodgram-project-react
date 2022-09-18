from django.db import models

from .validators import hex_color_validator
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
        validators=[hex_color_validator],
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
    value = models.PositiveSmallIntegerField(
        verbose_name="Количество",
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
        on_delete=models.CASCADE,
        null=False,
        related_name="ingridients",
        db_index=True,
    )
    tags = models.ManyToManyField(
        Tag,
        on_delete=models.SET_NULL,
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
                fields=["author", "name", "ingredients"],
            ),
            models.UniqueConstraint(
                name="author_recipe_unique",
                fields=["author", "ingredients"],
            ),
            models.UniqueConstraint(
                name="author_recipe_unique",
                fields=["name", "ingredients"],
            ),
        ]
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Follow(models.Model):
    """Модель подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
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
    )
    favourite = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favourite",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "favourite"], name="unique_favourites"
            )
        ]
        verbose_name = "Избранное"
