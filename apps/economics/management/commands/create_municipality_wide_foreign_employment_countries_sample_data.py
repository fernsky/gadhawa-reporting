"""
Management command to create sample data for Municipality Wide Foreign Employment Countries.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.economics.models import MunicipalityWideForeignEmploymentCountries

SAMPLE_DATA = [
    {"country": "AUSTRALIA", "population": 9 + 1 + 6 + 2 + 1},
    {"country": "NORTH_KOREA", "population": 4 + 1 + 1 + 2 + 1},
    {"country": "QATAR", "population": 20 + 6 + 18 + 33 + 60 + 38 + 48 + 1},
    {"country": "OTHER", "population": 12 + 11 + 8 + 1 + 12 + 18 + 12 + 2},
    {"country": "COLOMBIA", "population": 2 + 1},
    {"country": "CANADA", "population": 4 + 1 + 5 + 5},
    {"country": "CUBA", "population": 1},
    {"country": "JAPAN", "population": 10 + 3 + 12 + 15 + 9 + 5 + 9},
    {"country": "JORDAN", "population": 3 + 2},
    {"country": "SOUTH_AFRICA", "population": 1 + 5 + 2 + 2},
    {"country": "SOUTH_KOREA", "population": 2 + 2 + 4 + 1 + 6 + 3},
    {"country": "DUBAI", "population": 59 + 13 + 42 + 60 + 65 + 87 + 81},
    {"country": "PORTUGAL", "population": 1 + 3 + 10 + 5},
    {"country": "POLAND", "population": 1 + 2 + 2 + 1 + 2 + 1},
    {"country": "INDIA", "population": 343 + 99 + 264 + 241 + 181 + 311 + 175 + 43},
    {"country": "MONGOLIA", "population": 2 + 2},
    {"country": "MALAYSIA", "population": 83 + 43 + 40 + 46 + 34 + 66 + 51 + 1},
    {"country": "MALDIVES", "population": 3 + 2 + 2 + 2},
    {"country": "MOROCCO", "population": 1},
    {"country": "MAURITIUS", "population": 6 + 3 + 2 + 13 + 3},
    {"country": "YEMEN", "population": 3 + 2 + 1 + 2 + 2},
    {"country": "ROMANIA", "population": 11 + 2 + 1 + 3 + 5 + 7 + 1},
    {"country": "UNITED_STATES_OF_AMERICA", "population": 3 + 4 + 15 + 6 + 13 + 5 + 5},
    {"country": "SAUDI_ARABIA", "population": 37 + 29 + 34 + 55 + 62 + 94 + 79 + 6},
    {"country": "SYRIA", "population": 4},
    {"country": "SIERRA_LEONE", "population": 1},
    {"country": "AZERBAIJAN", "population": 1},
    {"country": "CROATIA", "population": 2 + 1 + 9 + 1},
    {"country": "NEW_ZEALAND", "population": 1},
    {"country": "WELLS", "population": 1 + 2},
    {"country": "UKRAINE", "population": 2 + 5},
    {"country": "BOSNIA", "population": 1},
    {"country": "HONG_KONG", "population": 3},
    {"country": "NEPAL", "population": 1},
    {"country": "PAKISTAN", "population": 4},
    {"country": "FAWNS", "population": 1},
    {"country": "BANGLADESH", "population": 1},
    {"country": "SWITZERLAND", "population": 1},
    {"country": "CONGO", "population": 1},
    {"country": "GREECE", "population": 3 + 2},
    {"country": "NIGER", "population": 1},
    {"country": "NIGERIA", "population": 4},
    {"country": "NAMIBIA", "population": 1},
    {"country": "MALTA", "population": 2 + 1},
    {"country": "SRIDAN", "population": 1},
    {"country": "RUSSIA", "population": 1 + 2},
    {"country": "UNITED_KINGDOM_OF_GREAT_BRITAIN", "population": 1 + 2},
    {"country": "UNITED_ARAB_EMIRATES", "population": 1},
    {"country": "CYPRUS", "population": 1 + 4},
    {"country": "SOMALIA", "population": 1},
    {"country": "SAN_MARINO", "population": 1},
    {"country": "PARAGUAY", "population": 3},
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
