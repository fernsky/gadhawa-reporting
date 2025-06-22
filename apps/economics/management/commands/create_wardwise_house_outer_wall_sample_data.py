"""
Management command to create sample data for Ward Wise House Outer Wall.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.economics.models import WardWiseHouseholdOuterWall, OuterWallTypeChoice

SAMPLE_DATA = [
    {"ward_number": 1, "wall_type": "BAMBOO", "households": 34},
    {"ward_number": 1, "wall_type": "CEMENT_JOINED", "households": 133},
    {"ward_number": 1, "wall_type": "MUD_JOINED", "households": 832},
    {"ward_number": 1, "wall_type": "TIN", "households": 22},
    {"ward_number": 1, "wall_type": "WOOD", "households": 23},
    {"ward_number": 2, "wall_type": "BAMBOO", "households": 7},
    {"ward_number": 2, "wall_type": "CEMENT_JOINED", "households": 68},
    {"ward_number": 2, "wall_type": "MUD_JOINED", "households": 855},
    {"ward_number": 2, "wall_type": "TIN", "households": 2},
    {"ward_number": 2, "wall_type": "WOOD", "households": 6},
    {"ward_number": 3, "wall_type": "BAMBOO", "households": 6},
    {"ward_number": 3, "wall_type": "CEMENT_JOINED", "households": 33},
    {"ward_number": 3, "wall_type": "MUD_JOINED", "households": 576},
    {"ward_number": 3, "wall_type": "TIN", "households": 8},
    {"ward_number": 3, "wall_type": "WOOD", "households": 16},
    {"ward_number": 4, "wall_type": "BAMBOO", "households": 8},
    {"ward_number": 4, "wall_type": "CEMENT_JOINED", "households": 93},
    {"ward_number": 4, "wall_type": "MUD_JOINED", "households": 735},
    {"ward_number": 4, "wall_type": "TIN", "households": 6},
    {"ward_number": 4, "wall_type": "WOOD", "households": 6},
    {"ward_number": 5, "wall_type": "BAMBOO", "households": 15},
    {"ward_number": 5, "wall_type": "CEMENT_JOINED", "households": 87},
    {"ward_number": 5, "wall_type": "MUD_JOINED", "households": 581},
    {"ward_number": 5, "wall_type": "TIN", "households": 5},
    {"ward_number": 5, "wall_type": "WOOD", "households": 31},
    {"ward_number": 6, "wall_type": "BAMBOO", "households": 19},
    {"ward_number": 6, "wall_type": "CEMENT_JOINED", "households": 26},
    {"ward_number": 6, "wall_type": "MUD_JOINED", "households": 783},
    {"ward_number": 6, "wall_type": "TIN", "households": 2},
    {"ward_number": 6, "wall_type": "WOOD", "households": 34},
    {"ward_number": 7, "wall_type": "BAMBOO", "households": 26},
    {"ward_number": 7, "wall_type": "CEMENT_JOINED", "households": 31},
    {"ward_number": 7, "wall_type": "MUD_JOINED", "households": 499},
    {"ward_number": 7, "wall_type": "TIN", "households": 11},
    {"ward_number": 7, "wall_type": "WOOD", "households": 20},
]


class Command(BaseCommand):
    help = "Create sample data for Ward Wise House Outer Wall"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            WardWiseHouseholdOuterWall.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing data cleared."))
        with transaction.atomic():
            for entry in SAMPLE_DATA:
                WardWiseHouseholdOuterWall.objects.update_or_create(
                    ward_number=entry["ward_number"],
                    wall_type=entry["wall_type"],
                    defaults={"households": entry["households"]},
                )
        self.stdout.write(
            self.style.SUCCESS("Sample data for Ward Wise House Outer Wall created.")
        )
