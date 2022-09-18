from django.db import models

from recipes.models import Recipe
from users.models import User


class ShoppingCart(models.Model):
    """Модель списков покупок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
    )
    shopping_cart = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="Shopping_cart",
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "shopping_cart"], name="unique_shopping_cart"
            )
        ]
        ordering = ("-pub_date",)
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
