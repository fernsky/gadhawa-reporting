"""
Management command to create sample data for Ward Wise House Ownership.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.economics.models import WardWiseHouseOwnership, HouseOwnershipTypeChoice

SAMPLE_DATA = [
    {"ward_number": 1, "ownership_type": "OTHER", "households": 10},
    {"ward_number": 1, "ownership_type": "PRIVATE", "households": 1105},
    {"ward_number": 1, "ownership_type": "RENT", "households": 24},
    {"ward_number": 2, "ownership_type": "OTHER", "households": 4},
    {"ward_number": 2, "ownership_type": "PRIVATE", "households": 907},
    {"ward_number": 2, "ownership_type": "RENT", "households": 6},
    {"ward_number": 2, "ownership_type": "INSTITUTIONAL", "households": 1},
    {"ward_number": 3, "ownership_type": "PRIVATE", "households": 564},
    {"ward_number": 4, "ownership_type": "PRIVATE", "households": 845},
    {"ward_number": 4, "ownership_type": "RENT", "households": 3},
    {"ward_number": 5, "ownership_type": "PRIVATE", "households": 710},
    {"ward_number": 5, "ownership_type": "RENT", "households": 9},
    {"ward_number": 6, "ownership_type": "PRIVATE", "households": 858},
    {"ward_number": 6, "ownership_type": "RENT", "households": 4},
    {"ward_number": 6, "ownership_type": "INSTITUTIONAL", "households": 2},
    {"ward_number": 7, "ownership_type": "OTHER", "households": 12},
    {"ward_number": 7, "ownership_type": "PRIVATE", "households": 553},
    {"ward_number": 7, "ownership_type": "RENT", "households": 20},
    {"ward_number": 7, "ownership_type": "INSTITUTIONAL", "households": 2},
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
