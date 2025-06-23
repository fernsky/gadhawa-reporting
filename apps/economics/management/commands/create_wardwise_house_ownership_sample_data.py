"""
Management command to create sample data for Ward Wise House Ownership.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.economics.models import WardWiseHouseOwnership, HouseOwnershipTypeChoice

SAMPLE_DATA = [
    {"ward_number": 1, "ownership_type": "PRIVATE", "households": 1713},
    {"ward_number": 1, "ownership_type": "RENT", "households": 22},
    {"ward_number": 2, "ownership_type": "PRIVATE", "households": 1196},
    {"ward_number": 2, "ownership_type": "RENT", "households": 5},
    {"ward_number": 3, "ownership_type": "PRIVATE", "households": 1146},
    {"ward_number": 3, "ownership_type": "RENT", "households": 147},
    {"ward_number": 3, "ownership_type": "INSTITUTIONAL", "households": 1},
    {"ward_number": 4, "ownership_type": "PRIVATE", "households": 1289},
    {"ward_number": 4, "ownership_type": "RENT", "households": 11},
    {"ward_number": 5, "ownership_type": "PRIVATE", "households": 1504},
    {"ward_number": 5, "ownership_type": "RENT", "households": 16},
    {"ward_number": 5, "ownership_type": "INSTITUTIONAL", "households": 2},
    {"ward_number": 6, "ownership_type": "PRIVATE", "households": 1688},
    {"ward_number": 6, "ownership_type": "RENT", "households": 71},
    {"ward_number": 6, "ownership_type": "INSTITUTIONAL", "households": 2},
    {"ward_number": 7, "ownership_type": "PRIVATE", "households": 1347},
    {"ward_number": 7, "ownership_type": "RENT", "households": 10},
    {"ward_number": 8, "ownership_type": "PRIVATE", "households": 196},
]


class Command(BaseCommand):
    help = "Create sample data for Ward Wise House Ownership"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            WardWiseHouseOwnership.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing data cleared."))
        with transaction.atomic():
            for entry in SAMPLE_DATA:
                WardWiseHouseOwnership.objects.update_or_create(
                    ward_number=entry["ward_number"],
                    ownership_type=entry["ownership_type"],
                    defaults={"households": entry["households"]},
                )
        self.stdout.write(
            self.style.SUCCESS("Sample data for Ward Wise House Ownership created.")
        )
