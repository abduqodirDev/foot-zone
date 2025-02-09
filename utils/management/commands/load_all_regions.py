import json

from django.core.management import BaseCommand

from utils.models import Viloyat, Tuman
from core.settings import BASE_DIR


class Command(BaseCommand):
    help = "load all viloyats"

    def handle(self, *args, **options):
        try:
            with open(str(BASE_DIR) + "/data/regions.json", encoding='utf-8') as f:
                countries = json.load(f)
                regions = countries['regions']
                for country in regions:
                    Viloyat.objects.get_or_create(name=country['name'])

            self.stdout.write(self.style.SUCCESS("Countries loaded successfully"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

