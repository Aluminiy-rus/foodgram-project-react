from django.db import models
from django.utils.html import format_html

from users.models import User


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=256,
        verbose_name="Тег",
        unique=True,
    )
    hex_colour = models.CharField(
        max_length=7,
        default="#ffffff"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def colored_name(self):
        """словестное наименование цвета"""
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.hexcolor,
        )

    def __str__(self):
        return self.name


class Ingridients(models.Model):
    """Модель ингридиентов"""
    
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
        unique=True,
    )
    value = models.FloatField(
        verbose_name="Количество",
    )
    units = models.CharField(
        max_length=256,
        verbose_name="Еденицы измерения",
        unique=True,
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Модель рецептов"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="recipes",
        db_index=True,
    )
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
        unique=True,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipies/',
        blank=True,
    )
    description = models.CharField(
        max_length=400,
        verbose_name="Текстовое описание",
        null=True,
    )
    ingridients = models.ManyToManyField(
        Ingridients,
        null=False,
        related_name="ingridients",
    )
    tag = models.ManyToManyField(
        Tag,
        related_name="tag",
    )
    сooking_time = models.TimeField(
        verbose_name="Время приготовления в минутах",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Follow(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_follow')
        ]
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'



class Favourites(models.Model):
    """Модель избранного"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_adding',
    )
    favourites = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favourite',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user_adding', 'favourites'],
            name='unique_favourites')
        ]
        verbose_name = 'Избранное'


class ShoppingList(models.Model):
    """Модель списка покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer',
    )
    shopping_list = models.ManyToManyField(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shopping_list',
    )
    
    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['buyer', 'shopping_list'],
            name='unique_shopping_list')
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'