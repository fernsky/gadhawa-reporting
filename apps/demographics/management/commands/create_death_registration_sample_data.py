"""
Management command to create death registration demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import (
    WardAgeGenderWiseDeceasedPopulation,
    AgeGroupChoice,
    GenderChoice,
)

# Paste your data here or load from a file
SAMPLE_DATA = [
    {"ward_number": 1, "age_group": "AGE_0_4", "gender": "MALE", "deceased_count": 2},
    {"ward_number": 1, "age_group": "AGE_10_14", "gender": "MALE", "deceased_count": 1},
    {"ward_number": 1, "age_group": "AGE_15_19", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 1,
        "age_group": "AGE_40_44",
        "gender": "FEMALE",
        "deceased_count": 3,
    },
    {
        "ward_number": 1,
        "age_group": "AGE_50_54",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 1, "age_group": "AGE_50_54", "gender": "MALE", "deceased_count": 3},
    {"ward_number": 1, "age_group": "AGE_5_9", "gender": "MALE", "deceased_count": 2},
    {
        "ward_number": 1,
        "age_group": "AGE_60_64",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 1, "age_group": "AGE_60_64", "gender": "MALE", "deceased_count": 1},
    {"ward_number": 1, "age_group": "AGE_70_74", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 1,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "MALE",
        "deceased_count": 3,
    },
    {"ward_number": 2, "age_group": "AGE_0_4", "gender": "FEMALE", "deceased_count": 2},
    {"ward_number": 2, "age_group": "AGE_0_4", "gender": "MALE", "deceased_count": 2},
    {"ward_number": 2, "age_group": "AGE_15_19", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 2,
        "age_group": "AGE_20_24",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {
        "ward_number": 2,
        "age_group": "AGE_25_29",
        "gender": "FEMALE",
        "deceased_count": 4,
    },
    {"ward_number": 2, "age_group": "AGE_25_29", "gender": "MALE", "deceased_count": 1},
    {"ward_number": 2, "age_group": "AGE_35_39", "gender": "MALE", "deceased_count": 3},
    {
        "ward_number": 2,
        "age_group": "AGE_45_49",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {
        "ward_number": 2,
        "age_group": "AGE_50_54",
        "gender": "FEMALE",
        "deceased_count": 2,
    },
    {"ward_number": 2, "age_group": "AGE_50_54", "gender": "MALE", "deceased_count": 2},
    {
        "ward_number": 2,
        "age_group": "AGE_55_59",
        "gender": "FEMALE",
        "deceased_count": 2,
    },
    {"ward_number": 2, "age_group": "AGE_55_59", "gender": "MALE", "deceased_count": 5},
    {"ward_number": 2, "age_group": "AGE_5_9", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 2,
        "age_group": "AGE_60_64",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 2, "age_group": "AGE_60_64", "gender": "MALE", "deceased_count": 1},
    {"ward_number": 2, "age_group": "AGE_65_69", "gender": "MALE", "deceased_count": 4},
    {
        "ward_number": 2,
        "age_group": "AGE_70_74",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 2, "age_group": "AGE_70_74", "gender": "MALE", "deceased_count": 2},
    {
        "ward_number": 2,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "FEMALE",
        "deceased_count": 3,
    },
    {
        "ward_number": 2,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "MALE",
        "deceased_count": 5,
    },
    {
        "ward_number": 3,
        "age_group": "AGE_25_29",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {
        "ward_number": 3,
        "age_group": "AGE_50_54",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {
        "ward_number": 3,
        "age_group": "AGE_60_64",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 3, "age_group": "AGE_65_69", "gender": "MALE", "deceased_count": 2},
    {
        "ward_number": 3,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {
        "ward_number": 3,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "MALE",
        "deceased_count": 1,
    },
    {"ward_number": 4, "age_group": "AGE_0_4", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 4,
        "age_group": "AGE_10_14",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {
        "ward_number": 4,
        "age_group": "AGE_50_54",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 4, "age_group": "AGE_60_64", "gender": "MALE", "deceased_count": 2},
    {
        "ward_number": 4,
        "age_group": "AGE_65_69",
        "gender": "FEMALE",
        "deceased_count": 2,
    },
    {
        "ward_number": 4,
        "age_group": "AGE_70_74",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 4, "age_group": "AGE_70_74", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 4,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "MALE",
        "deceased_count": 5,
    },
    {
        "ward_number": 5,
        "age_group": "AGE_25_29",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 5, "age_group": "AGE_45_49", "gender": "MALE", "deceased_count": 1},
    {"ward_number": 5, "age_group": "AGE_55_59", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 5,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "FEMALE",
        "deceased_count": 3,
    },
    {
        "ward_number": 5,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "MALE",
        "deceased_count": 2,
    },
    {"ward_number": 6, "age_group": "AGE_0_4", "gender": "FEMALE", "deceased_count": 1},
    {"ward_number": 6, "age_group": "AGE_15_19", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 6,
        "age_group": "AGE_20_24",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 6, "age_group": "AGE_20_24", "gender": "MALE", "deceased_count": 1},
    {"ward_number": 6, "age_group": "AGE_45_49", "gender": "MALE", "deceased_count": 1},
    {"ward_number": 6, "age_group": "AGE_65_69", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 6,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "FEMALE",
        "deceased_count": 3,
    },
    {
        "ward_number": 6,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "MALE",
        "deceased_count": 2,
    },
    {"ward_number": 7, "age_group": "AGE_0_4", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 7,
        "age_group": "AGE_10_14",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {
        "ward_number": 7,
        "age_group": "AGE_15_19",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 7, "age_group": "AGE_25_29", "gender": "MALE", "deceased_count": 1},
    {"ward_number": 7, "age_group": "AGE_30_34", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 7,
        "age_group": "AGE_40_44",
        "gender": "FEMALE",
        "deceased_count": 1,
    },
    {"ward_number": 7, "age_group": "AGE_55_59", "gender": "MALE", "deceased_count": 1},
    {"ward_number": 7, "age_group": "AGE_60_64", "gender": "MALE", "deceased_count": 1},
    {
        "ward_number": 7,
        "age_group": "AGE_75_AND_ABOVE",
        "gender": "MALE",
        "deceased_count": 1,
    },
]


class Command(BaseCommand):
    help = (
        "Create death registration demographics data based on actual municipality data"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            WardAgeGenderWiseDeceasedPopulation.objects.all().delete()
            self.stdout.write(
                self.style.WARNING("Existing death registration data cleared.")
            )

        self.stdout.write(
            "Creating death registration demographics data based on actual municipality data..."
        )
        with transaction.atomic():
            for entry in SAMPLE_DATA:
                WardAgeGenderWiseDeceasedPopulation.objects.create(
                    ward_number=entry["ward_number"],
                    age_group=entry["age_group"],
                    gender=entry["gender"],
                    deceased_population=entry["deceased_count"],
                )
        self.stdout.write(self.style.SUCCESS("Death registration sample data created."))
