# Generated by Django 3.2.15 on 2022-10-07 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20221007_1901'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='recipeingredientamount',
            name='recipe_ingredient_amount',
        ),
        migrations.AlterField(
            model_name='recipeingredientamount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipe_ingredient_amount', to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='recipeingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredient_amount', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredientamount',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient', 'amount'), name='unique_recipe_ingredient_amount'),
        ),
    ]
