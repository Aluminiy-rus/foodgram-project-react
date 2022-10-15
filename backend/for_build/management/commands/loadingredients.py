import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "load ingredients to base from `../data/ingredients.csv`"

    def handle(self, *args, **kwargs):
        with open("data/ingredients.csv", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                if not Ingredient.objects.filter(name=row[0]).exists():
                    print("add ingredient {}".format(row[0]))
                    Ingredient.objects.update_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
            print("ingredients added successfully")
