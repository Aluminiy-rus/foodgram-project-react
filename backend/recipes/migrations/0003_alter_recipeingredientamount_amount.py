# Generated by Django 3.2.15 on 2022-10-05 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipeingredientamount",
            name="amount",
            field=models.PositiveSmallIntegerField(verbose_name="Количество"),
        ),
    ]