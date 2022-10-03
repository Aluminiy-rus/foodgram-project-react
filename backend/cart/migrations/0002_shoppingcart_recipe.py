# Generated by Django 3.2.15 on 2022-10-03 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cart", "0001_initial"),
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shoppingcart",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart_recipe",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
    ]
