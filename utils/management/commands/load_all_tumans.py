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
                regions = countries['districts']
                for country in regions:
                    viloyat_id = country['region_id'] + 13
                    viloyat = Viloyat.objects.get(id=viloyat_id)
                    Tuman.objects.get_or_create(name=country['name'], viloyat=viloyat)

            self.stdout.write(self.style.SUCCESS("Countries loaded successfully"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

