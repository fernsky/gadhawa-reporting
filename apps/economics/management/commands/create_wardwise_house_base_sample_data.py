"""
Management command to create sample data for Ward Wise House Base.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.economics.models import WardWiseHouseholdBase, HouseholdBaseTypeChoice

SAMPLE_DATA = [
    {"ward_number": 1, "base_type": "CEMENT_JOINED", "households": 104},
    {"ward_number": 1, "base_type": "CONCRETE_PILLAR", "households": 35},
    {"ward_number": 1, "base_type": "MUD_JOINED", "households": 818},
    {"ward_number": 1, "base_type": "OTHER", "households": 1},
    {"ward_number": 1, "base_type": "WOOD_POLE", "households": 86},
    {"ward_number": 2, "base_type": "CEMENT_JOINED", "households": 29},
    {"ward_number": 2, "base_type": "CONCRETE_PILLAR", "households": 10},
    {"ward_number": 2, "base_type": "MUD_JOINED", "households": 890},
    {"ward_number": 2, "base_type": "OTHER", "households": 1},
    {"ward_number": 2, "base_type": "WOOD_POLE", "households": 8},
    {"ward_number": 3, "base_type": "CEMENT_JOINED", "households": 30},
    {"ward_number": 3, "base_type": "CONCRETE_PILLAR", "households": 3},
    {"ward_number": 3, "base_type": "MUD_JOINED", "households": 590},
    {"ward_number": 3, "base_type": "OTHER", "households": 1},
    {"ward_number": 3, "base_type": "WOOD_POLE", "households": 15},
    {"ward_number": 4, "base_type": "CEMENT_JOINED", "households": 74},
    {"ward_number": 4, "base_type": "CONCRETE_PILLAR", "households": 17},
    {"ward_number": 4, "base_type": "MUD_JOINED", "households": 743},
    {"ward_number": 4, "base_type": "WOOD_POLE", "households": 14},
    {"ward_number": 5, "base_type": "CEMENT_JOINED", "households": 92},
    {"ward_number": 5, "base_type": "CONCRETE_PILLAR", "households": 14},
    {"ward_number": 5, "base_type": "MUD_JOINED", "households": 583},
    {"ward_number": 5, "base_type": "OTHER", "households": 5},
    {"ward_number": 5, "base_type": "WOOD_POLE", "households": 25},
    {"ward_number": 6, "base_type": "CEMENT_JOINED", "households": 17},
    {"ward_number": 6, "base_type": "CONCRETE_PILLAR", "households": 13},
    {"ward_number": 6, "base_type": "MUD_JOINED", "households": 790},
    {"ward_number": 6, "base_type": "OTHER", "households": 4},
    {"ward_number": 6, "base_type": "WOOD_POLE", "households": 40},
    {"ward_number": 7, "base_type": "CEMENT_JOINED", "households": 26},
    {"ward_number": 7, "base_type": "CONCRETE_PILLAR", "households": 16},
    {"ward_number": 7, "base_type": "MUD_JOINED", "households": 492},
    {"ward_number": 7, "base_type": "WOOD_POLE", "households": 53},
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
