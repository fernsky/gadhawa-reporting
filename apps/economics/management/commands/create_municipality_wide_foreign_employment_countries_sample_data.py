"""
Management command to create sample data for Municipality Wide Foreign Employment Countries.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.economics.models import MunicipalityWideForeignEmploymentCountries

SAMPLE_DATA = [
    {"country": "AZERBAIJAN", "population": 1},
    {"country": "BAHRAIN", "population": 15},
    {"country": "BELGIUM", "population": 1},
    {"country": "BRUNEI", "population": 5},
    {"country": "BULGARIA", "population": 2},
    {"country": "CAMEROON", "population": 5},
    {"country": "CANADA", "population": 2},
    {"country": "CECILS", "population": 1},
    {"country": "COSTA_RICA", "population": 1},
    {"country": "CROATIA", "population": 1},
    {"country": "CYPRUS", "population": 1},
    {"country": "DUBAI", "population": 271},
    {"country": "GREECE", "population": 2},
    {"country": "INDIA", "population": 626},
    {"country": "JAPAN", "population": 40},
    {"country": "KATHMANDU", "population": 7},
    {"country": "KOSOVO", "population": 1},
    {"country": "MALAYSIA", "population": 234},
    {"country": "MALDIVES", "population": 4},
    {"country": "MALTA", "population": 1},
    {"country": "MAURITIUS", "population": 258},
    {"country": "MEXICO", "population": 1},
    {"country": "MYANMAR", "population": 4},
    {"country": "NIGER", "population": 1},
    {"country": "NORTH_KOREA", "population": 9},
    {"country": "NORWAY", "population": 1},
    {"country": "OTHER", "population": 37},
    {"country": "PAKISTAN", "population": 5},
    {"country": "PERU", "population": 1},
    {"country": "POLAND", "population": 4},
    {"country": "PORTUGAL", "population": 8},
    {"country": "QATAR", "population": 346},
    {"country": "ROMANIA", "population": 28},
    {"country": "SAN_MARINO", "population": 1},
    {"country": "SAUDI_ARABIA", "population": 670},
    {"country": "SOUTH_AFRICA", "population": 5},
    {"country": "SOUTH_KOREA", "population": 14},
    {"country": "TURKEY", "population": 11},
    {"country": "UKRAINE", "population": 2},
    {"country": "UNITED_ARAB_EMIRATES", "population": 7},
    {"country": "UNITED_KINGDOM_OF_GREAT_BRITAIN", "population": 8},
    {"country": "UNITED_STATES_OF_AMERICA", "population": 9},
    {"country": "YEMEN", "population": 2},
]


class Command(BaseCommand):
    help = "Create sample data for Municipality Wide Foreign Employment Countries"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            MunicipalityWideForeignEmploymentCountries.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing data cleared."))
        with transaction.atomic():
            for entry in SAMPLE_DATA:
                MunicipalityWideForeignEmploymentCountries.objects.update_or_create(
                    country=entry["country"],
                    defaults={"population": entry["population"]},
                )
        self.stdout.write(
            self.style.SUCCESS(
                "Sample data for Municipality Wide Foreign Employment Countries created."
            )
        )
