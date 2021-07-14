import csv
from typing import Any, Optional

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        with open('recipes/data/ingredients.csv', encoding='utf8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, unit = row
                Ingredient.objects.get_or_create(
                    name=name.capitalize(), unit=unit
                )
