"""
Management command to create sample data for Ward Wise House Base.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.economics.models import WardWiseHouseholdBase, HouseholdBaseTypeChoice

SAMPLE_DATA = [
    {"ward_number": 1, "base_type": "CEMENT_JOINED", "households": 388},
    {"ward_number": 1, "base_type": "CONCRETE_PILLAR", "households": 531},
    {"ward_number": 1, "base_type": "MUD_JOINED", "households": 93},
    {"ward_number": 1, "base_type": "OTHER", "households": 74},
    {"ward_number": 1, "base_type": "WOOD_POLE", "households": 649},
    {"ward_number": 2, "base_type": "CEMENT_JOINED", "households": 303},
    {"ward_number": 2, "base_type": "CONCRETE_PILLAR", "households": 304},
    {"ward_number": 2, "base_type": "MUD_JOINED", "households": 283},
    {"ward_number": 2, "base_type": "OTHER", "households": 1},
    {"ward_number": 2, "base_type": "WOOD_POLE", "households": 310},
    {"ward_number": 3, "base_type": "CEMENT_JOINED", "households": 283},
    {"ward_number": 3, "base_type": "CONCRETE_PILLAR", "households": 598},
    {"ward_number": 3, "base_type": "MUD_JOINED", "households": 215},
    {"ward_number": 3, "base_type": "OTHER", "households": 13},
    {"ward_number": 3, "base_type": "WOOD_POLE", "households": 185},
    {"ward_number": 4, "base_type": "CEMENT_JOINED", "households": 271},
    {"ward_number": 4, "base_type": "CONCRETE_PILLAR", "households": 563},
    {"ward_number": 4, "base_type": "MUD_JOINED", "households": 144},
    {"ward_number": 4, "base_type": "OTHER", "households": 2},
    {"ward_number": 4, "base_type": "WOOD_POLE", "households": 320},
    {"ward_number": 5, "base_type": "CEMENT_JOINED", "households": 253},
    {"ward_number": 5, "base_type": "CONCRETE_PILLAR", "households": 533},
    {"ward_number": 5, "base_type": "MUD_JOINED", "households": 165},
    {"ward_number": 5, "base_type": "OTHER", "households": 41},
    {"ward_number": 5, "base_type": "WOOD_POLE", "households": 530},
    {"ward_number": 6, "base_type": "CEMENT_JOINED", "households": 543},
    {"ward_number": 6, "base_type": "CONCRETE_PILLAR", "households": 521},
    {"ward_number": 6, "base_type": "MUD_JOINED", "households": 240},
    {"ward_number": 6, "base_type": "OTHER", "households": 65},
    {"ward_number": 6, "base_type": "WOOD_POLE", "households": 392},
    {"ward_number": 7, "base_type": "CEMENT_JOINED", "households": 516},
    {"ward_number": 7, "base_type": "CONCRETE_PILLAR", "households": 324},
    {"ward_number": 7, "base_type": "MUD_JOINED", "households": 193},
    {"ward_number": 7, "base_type": "OTHER", "households": 82},
    {"ward_number": 7, "base_type": "WOOD_POLE", "households": 242},
    {"ward_number": 8, "base_type": "CEMENT_JOINED", "households": 65},
    {"ward_number": 8, "base_type": "CONCRETE_PILLAR", "households": 10},
    {"ward_number": 8, "base_type": "MUD_JOINED", "households": 57},
    {"ward_number": 8, "base_type": "OTHER", "households": 1},
    {"ward_number": 8, "base_type": "WOOD_POLE", "households": 63},
]


class Command(BaseCommand):
    help = "Create sample data for Ward Wise House Base"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            WardWiseHouseholdBase.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing data cleared."))
        with transaction.atomic():
            for entry in SAMPLE_DATA:
                WardWiseHouseholdBase.objects.update_or_create(
                    ward_number=entry["ward_number"],
                    base_type=entry["base_type"],
                    defaults={"households": entry["households"]},
                )
        self.stdout.write(
            self.style.SUCCESS("Sample data for Ward Wise House Base created.")
        )
