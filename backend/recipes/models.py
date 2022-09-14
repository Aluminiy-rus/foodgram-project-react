from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=256,
        verbose_name="Тег",
        unique=True,
        db_index=True,
    )
    color = models.CharField(
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

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиентов"""
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
        unique=True,
        db_index=True,
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
        ordering = ['name']
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
        verbose_name='Картинка',
        upload_to='recipies/',
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
        related_name="tags",
        db_index=True,
    )
    сooking_time = models.TimeField(
        verbose_name="Время приготовления в минутах",
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='author_recipe_unique',
                fields=['author', 'name'],
            ),
        ]
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class UniqueRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_recipe',
                fields=['recipe', 'ingredient', 'amount'],
            ),
        ]


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
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'



class Favourite(models.Model):
    """Модель избранного"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )
    favourite = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'favourite'],
            name='unique_favourites')
        ]
        verbose_name = 'Избранное'


class ShoppingCart(models.Model):
    """Модель списков покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )
    shopping_cart = models.ManyToManyField(
        Recipe,
        on_delete=models.CASCADE,
        related_name='Shopping_cart',
    )
    
    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'shopping_cart'],
            name='unique_shopping_cart')
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'