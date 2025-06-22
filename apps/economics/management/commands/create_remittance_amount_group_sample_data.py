"""
Management command to create sample data for Ward Wise Remittance Amount Group.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.economics.models import WardWiseRemittance

# Mapping from old group names to new enum values
AMOUNT_GROUP_MAP = {
    "NO_REMITTANCE": "RS_0_TO_49999",
    "BELOW_50K": "RS_0_TO_49999",
    "RS_50K_TO_100K": "RS_50000_TO_99999",
    "RS_100K_TO_200K": "RS_100000_TO_149999",
    "RS_200K_TO_500K": "RS_200000_TO_249999",  # You may want to split this if you have more granularity
    "ABOVE_500K": "RS_500000_PLUS",
}

SAMPLE_DATA = [
    {"ward_number": 1, "amount_group": "NO_REMITTANCE", "sending_population": 301},
    {"ward_number": 1, "amount_group": "BELOW_50K", "sending_population": 24},
    {"ward_number": 1, "amount_group": "RS_50K_TO_100K", "sending_population": 7},
    {"ward_number": 1, "amount_group": "RS_100K_TO_200K", "sending_population": 9},
    {"ward_number": 1, "amount_group": "RS_200K_TO_500K", "sending_population": 16},
    {"ward_number": 1, "amount_group": "ABOVE_500K", "sending_population": 74},
    {"ward_number": 2, "amount_group": "NO_REMITTANCE", "sending_population": 6},
    {"ward_number": 2, "amount_group": "BELOW_50K", "sending_population": 90},
    {"ward_number": 2, "amount_group": "RS_50K_TO_100K", "sending_population": 36},
    {"ward_number": 2, "amount_group": "RS_100K_TO_200K", "sending_population": 53},
    {"ward_number": 2, "amount_group": "RS_200K_TO_500K", "sending_population": 82},
    {"ward_number": 2, "amount_group": "ABOVE_500K", "sending_population": 93},
    {"ward_number": 3, "amount_group": "NO_REMITTANCE", "sending_population": 9},
    {"ward_number": 3, "amount_group": "BELOW_50K", "sending_population": 13},
    {"ward_number": 3, "amount_group": "RS_50K_TO_100K", "sending_population": 24},
    {"ward_number": 3, "amount_group": "RS_100K_TO_200K", "sending_population": 28},
    {"ward_number": 3, "amount_group": "RS_200K_TO_500K", "sending_population": 111},
    {"ward_number": 3, "amount_group": "ABOVE_500K", "sending_population": 59},
    {"ward_number": 4, "amount_group": "NO_REMITTANCE", "sending_population": 12},
    {"ward_number": 4, "amount_group": "BELOW_50K", "sending_population": 71},
    {"ward_number": 4, "amount_group": "RS_50K_TO_100K", "sending_population": 76},
    {"ward_number": 4, "amount_group": "RS_100K_TO_200K", "sending_population": 70},
    {"ward_number": 4, "amount_group": "RS_200K_TO_500K", "sending_population": 128},
    {"ward_number": 4, "amount_group": "ABOVE_500K", "sending_population": 25},
    {"ward_number": 5, "amount_group": "NO_REMITTANCE", "sending_population": 92},
    {"ward_number": 5, "amount_group": "BELOW_50K", "sending_population": 22},
    {"ward_number": 5, "amount_group": "RS_50K_TO_100K", "sending_population": 29},
    {"ward_number": 5, "amount_group": "RS_100K_TO_200K", "sending_population": 26},
    {"ward_number": 5, "amount_group": "RS_200K_TO_500K", "sending_population": 51},
    {"ward_number": 5, "amount_group": "ABOVE_500K", "sending_population": 37},
    {"ward_number": 6, "amount_group": "NO_REMITTANCE", "sending_population": 43},
    {"ward_number": 6, "amount_group": "BELOW_50K", "sending_population": 39},
    {"ward_number": 6, "amount_group": "RS_50K_TO_100K", "sending_population": 43},
    {"ward_number": 6, "amount_group": "RS_100K_TO_200K", "sending_population": 41},
    {"ward_number": 6, "amount_group": "RS_200K_TO_500K", "sending_population": 33},
    {"ward_number": 6, "amount_group": "ABOVE_500K", "sending_population": 3},
    {"ward_number": 7, "amount_group": "NO_REMITTANCE", "sending_population": 80},
    {"ward_number": 7, "amount_group": "BELOW_50K", "sending_population": 18},
    {"ward_number": 7, "amount_group": "RS_50K_TO_100K", "sending_population": 12},
    {"ward_number": 7, "amount_group": "RS_100K_TO_200K", "sending_population": 44},
    {"ward_number": 7, "amount_group": "RS_200K_TO_500K", "sending_population": 37},
    {"ward_number": 7, "amount_group": "ABOVE_500K", "sending_population": 1},
    {"ward_number": 8, "amount_group": "NO_REMITTANCE", "sending_population": 0},
    {"ward_number": 8, "amount_group": "BELOW_50K", "sending_population": 0},
    {"ward_number": 8, "amount_group": "RS_50K_TO_100K", "sending_population": 0},
    {"ward_number": 8, "amount_group": "RS_100K_TO_200K", "sending_population": 0},
    {"ward_number": 8, "amount_group": "RS_200K_TO_500K", "sending_population": 0},
    {"ward_number": 8, "amount_group": "ABOVE_500K", "sending_population": 0},
    {"ward_number": 9, "amount_group": "NO_REMITTANCE", "sending_population": 0},
    {"ward_number": 9, "amount_group": "BELOW_50K", "sending_population": 0},
    {"ward_number": 9, "amount_group": "RS_50K_TO_100K", "sending_population": 0},
    {"ward_number": 9, "amount_group": "RS_100K_TO_200K", "sending_population": 0},
    {"ward_number": 9, "amount_group": "RS_200K_TO_500K", "sending_population": 0},
    {"ward_number": 9, "amount_group": "ABOVE_500K", "sending_population": 0},
]


class Command(BaseCommand):
    help = "Create sample data for Ward Wise Remittance Amount Group (mapped to enum)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            WardWiseRemittance.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing data cleared."))
        with transaction.atomic():
            for entry in SAMPLE_DATA:
                mapped_group = AMOUNT_GROUP_MAP.get(
                    entry["amount_group"], entry["amount_group"]
                )
                WardWiseRemittance.objects.update_or_create(
                    ward_number=entry["ward_number"],
                    amount_group=mapped_group,
                    defaults={"sending_population": entry["sending_population"]},
                )
        self.stdout.write(
            self.style.SUCCESS(
                "Sample data for Ward Wise Remittance Amount Group created (mapped to enum)."
            )
        )
