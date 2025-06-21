"""
Management command to create age-gender demographics data based on actual data
"""

import uuid
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import WardAgeWisePopulation, AgeGroupChoice, GenderChoice


class Command(BaseCommand):
    help = "Create age-gender demographics data based on actual municipality data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing age-gender data...")
            )
            WardAgeWisePopulation.objects.all().delete()

        self.stdout.write(
            "Creating age-gender demographics data based on actual municipality data..."
        )

        # Actual data from the JSON provided
        actual_data = [
            {
                "ward_number": 1,
                "age_group": "AGE_0_4",
                "gender": "FEMALE",
                "population": 384,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_0_4",
                "gender": "MALE",
                "population": 153,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_10_14",
                "gender": "FEMALE",
                "population": 329,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_10_14",
                "gender": "MALE",
                "population": 235,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_15_19",
                "gender": "FEMALE",
                "population": 287,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_15_19",
                "gender": "MALE",
                "population": 281,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_20_24",
                "gender": "FEMALE",
                "population": 272,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_20_24",
                "gender": "MALE",
                "population": 294,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_25_29",
                "gender": "FEMALE",
                "population": 234,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_25_29",
                "gender": "MALE",
                "population": 291,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_30_34",
                "gender": "FEMALE",
                "population": 210,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_30_34",
                "gender": "MALE",
                "population": 228,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_35_39",
                "gender": "FEMALE",
                "population": 160,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_35_39",
                "gender": "MALE",
                "population": 155,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_40_44",
                "gender": "FEMALE",
                "population": 161,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_40_44",
                "gender": "MALE",
                "population": 119,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_45_49",
                "gender": "FEMALE",
                "population": 103,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_45_49",
                "gender": "MALE",
                "population": 108,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_50_54",
                "gender": "FEMALE",
                "population": 117,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_50_54",
                "gender": "MALE",
                "population": 134,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_55_59",
                "gender": "FEMALE",
                "population": 89,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_55_59",
                "gender": "MALE",
                "population": 107,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_5_9",
                "gender": "FEMALE",
                "population": 336,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_5_9",
                "gender": "MALE",
                "population": 194,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_60_64",
                "gender": "FEMALE",
                "population": 63,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_60_64",
                "gender": "MALE",
                "population": 107,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_65_69",
                "gender": "FEMALE",
                "population": 52,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_65_69",
                "gender": "MALE",
                "population": 93,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_70_74",
                "gender": "FEMALE",
                "population": 55,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_70_74",
                "gender": "MALE",
                "population": 81,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "FEMALE",
                "population": 59,
            },
            {
                "ward_number": 1,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "MALE",
                "population": 112,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_0_4",
                "gender": "FEMALE",
                "population": 188,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_0_4",
                "gender": "MALE",
                "population": 175,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_10_14",
                "gender": "FEMALE",
                "population": 217,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_10_14",
                "gender": "MALE",
                "population": 239,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_15_19",
                "gender": "FEMALE",
                "population": 235,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_15_19",
                "gender": "MALE",
                "population": 249,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_20_24",
                "gender": "FEMALE",
                "population": 255,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_20_24",
                "gender": "MALE",
                "population": 263,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_25_29",
                "gender": "FEMALE",
                "population": 201,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_25_29",
                "gender": "MALE",
                "population": 151,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_30_34",
                "gender": "FEMALE",
                "population": 146,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_30_34",
                "gender": "MALE",
                "population": 138,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_35_39",
                "gender": "FEMALE",
                "population": 118,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_35_39",
                "gender": "MALE",
                "population": 118,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_40_44",
                "gender": "FEMALE",
                "population": 119,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_40_44",
                "gender": "MALE",
                "population": 96,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_45_49",
                "gender": "FEMALE",
                "population": 100,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_45_49",
                "gender": "MALE",
                "population": 70,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_50_54",
                "gender": "FEMALE",
                "population": 81,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_50_54",
                "gender": "MALE",
                "population": 79,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_55_59",
                "gender": "FEMALE",
                "population": 76,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_55_59",
                "gender": "MALE",
                "population": 70,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_5_9",
                "gender": "FEMALE",
                "population": 261,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_5_9",
                "gender": "MALE",
                "population": 222,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_60_64",
                "gender": "FEMALE",
                "population": 73,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_60_64",
                "gender": "MALE",
                "population": 49,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_65_69",
                "gender": "FEMALE",
                "population": 51,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_65_69",
                "gender": "MALE",
                "population": 41,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_70_74",
                "gender": "FEMALE",
                "population": 56,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_70_74",
                "gender": "MALE",
                "population": 33,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "FEMALE",
                "population": 50,
            },
            {
                "ward_number": 2,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "MALE",
                "population": 45,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_0_4",
                "gender": "FEMALE",
                "population": 177,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_0_4",
                "gender": "MALE",
                "population": 128,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_10_14",
                "gender": "FEMALE",
                "population": 182,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_10_14",
                "gender": "MALE",
                "population": 176,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_15_19",
                "gender": "FEMALE",
                "population": 173,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_15_19",
                "gender": "MALE",
                "population": 157,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_20_24",
                "gender": "FEMALE",
                "population": 189,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_20_24",
                "gender": "MALE",
                "population": 164,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_25_29",
                "gender": "FEMALE",
                "population": 131,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_25_29",
                "gender": "MALE",
                "population": 140,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_30_34",
                "gender": "FEMALE",
                "population": 121,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_30_34",
                "gender": "MALE",
                "population": 98,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_35_39",
                "gender": "FEMALE",
                "population": 88,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_35_39",
                "gender": "MALE",
                "population": 73,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_40_44",
                "gender": "FEMALE",
                "population": 92,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_40_44",
                "gender": "MALE",
                "population": 76,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_45_49",
                "gender": "FEMALE",
                "population": 61,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_45_49",
                "gender": "MALE",
                "population": 61,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_50_54",
                "gender": "FEMALE",
                "population": 65,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_50_54",
                "gender": "MALE",
                "population": 39,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_55_59",
                "gender": "FEMALE",
                "population": 35,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_55_59",
                "gender": "MALE",
                "population": 36,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_5_9",
                "gender": "FEMALE",
                "population": 178,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_5_9",
                "gender": "MALE",
                "population": 177,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_60_64",
                "gender": "FEMALE",
                "population": 43,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_60_64",
                "gender": "MALE",
                "population": 31,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_65_69",
                "gender": "FEMALE",
                "population": 25,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_65_69",
                "gender": "MALE",
                "population": 26,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_70_74",
                "gender": "FEMALE",
                "population": 24,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_70_74",
                "gender": "MALE",
                "population": 20,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "FEMALE",
                "population": 25,
            },
            {
                "ward_number": 3,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "MALE",
                "population": 27,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_0_4",
                "gender": "FEMALE",
                "population": 113,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_0_4",
                "gender": "MALE",
                "population": 141,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_10_14",
                "gender": "FEMALE",
                "population": 275,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_10_14",
                "gender": "MALE",
                "population": 203,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_15_19",
                "gender": "FEMALE",
                "population": 239,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_15_19",
                "gender": "MALE",
                "population": 186,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_20_24",
                "gender": "FEMALE",
                "population": 246,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_20_24",
                "gender": "MALE",
                "population": 203,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_25_29",
                "gender": "FEMALE",
                "population": 196,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_25_29",
                "gender": "MALE",
                "population": 176,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_30_34",
                "gender": "FEMALE",
                "population": 169,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_30_34",
                "gender": "MALE",
                "population": 140,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_35_39",
                "gender": "FEMALE",
                "population": 124,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_35_39",
                "gender": "MALE",
                "population": 121,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_40_44",
                "gender": "FEMALE",
                "population": 117,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_40_44",
                "gender": "MALE",
                "population": 102,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_45_49",
                "gender": "FEMALE",
                "population": 90,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_45_49",
                "gender": "MALE",
                "population": 73,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_50_54",
                "gender": "FEMALE",
                "population": 93,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_50_54",
                "gender": "MALE",
                "population": 80,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_55_59",
                "gender": "FEMALE",
                "population": 75,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_55_59",
                "gender": "MALE",
                "population": 55,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_5_9",
                "gender": "FEMALE",
                "population": 273,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_5_9",
                "gender": "MALE",
                "population": 208,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_60_64",
                "gender": "FEMALE",
                "population": 50,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_60_64",
                "gender": "MALE",
                "population": 54,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_65_69",
                "gender": "FEMALE",
                "population": 40,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_65_69",
                "gender": "MALE",
                "population": 40,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_70_74",
                "gender": "FEMALE",
                "population": 55,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_70_74",
                "gender": "MALE",
                "population": 40,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "FEMALE",
                "population": 46,
            },
            {
                "ward_number": 4,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "MALE",
                "population": 36,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_0_4",
                "gender": "FEMALE",
                "population": 89,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_0_4",
                "gender": "MALE",
                "population": 68,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_10_14",
                "gender": "FEMALE",
                "population": 212,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_10_14",
                "gender": "MALE",
                "population": 116,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_15_19",
                "gender": "FEMALE",
                "population": 237,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_15_19",
                "gender": "MALE",
                "population": 146,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_20_24",
                "gender": "FEMALE",
                "population": 220,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_20_24",
                "gender": "MALE",
                "population": 170,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_25_29",
                "gender": "FEMALE",
                "population": 165,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_25_29",
                "gender": "MALE",
                "population": 107,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_30_34",
                "gender": "FEMALE",
                "population": 152,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_30_34",
                "gender": "MALE",
                "population": 114,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_35_39",
                "gender": "FEMALE",
                "population": 139,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_35_39",
                "gender": "MALE",
                "population": 131,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_40_44",
                "gender": "FEMALE",
                "population": 118,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_40_44",
                "gender": "MALE",
                "population": 138,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_45_49",
                "gender": "FEMALE",
                "population": 100,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_45_49",
                "gender": "MALE",
                "population": 120,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_50_54",
                "gender": "FEMALE",
                "population": 61,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_50_54",
                "gender": "MALE",
                "population": 78,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_55_59",
                "gender": "FEMALE",
                "population": 54,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_55_59",
                "gender": "MALE",
                "population": 42,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_5_9",
                "gender": "FEMALE",
                "population": 154,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_5_9",
                "gender": "MALE",
                "population": 97,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_60_64",
                "gender": "FEMALE",
                "population": 49,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_60_64",
                "gender": "MALE",
                "population": 47,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_65_69",
                "gender": "FEMALE",
                "population": 38,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_65_69",
                "gender": "MALE",
                "population": 37,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_70_74",
                "gender": "FEMALE",
                "population": 54,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_70_74",
                "gender": "MALE",
                "population": 40,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "FEMALE",
                "population": 43,
            },
            {
                "ward_number": 5,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "MALE",
                "population": 70,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_0_4",
                "gender": "FEMALE",
                "population": 163,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_0_4",
                "gender": "MALE",
                "population": 160,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_10_14",
                "gender": "FEMALE",
                "population": 259,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_10_14",
                "gender": "MALE",
                "population": 219,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_15_19",
                "gender": "FEMALE",
                "population": 260,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_15_19",
                "gender": "MALE",
                "population": 233,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_20_24",
                "gender": "FEMALE",
                "population": 209,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_20_24",
                "gender": "MALE",
                "population": 218,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_25_29",
                "gender": "FEMALE",
                "population": 197,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_25_29",
                "gender": "MALE",
                "population": 170,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_30_34",
                "gender": "FEMALE",
                "population": 184,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_30_34",
                "gender": "MALE",
                "population": 176,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_35_39",
                "gender": "FEMALE",
                "population": 143,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_35_39",
                "gender": "MALE",
                "population": 111,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_40_44",
                "gender": "FEMALE",
                "population": 155,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_40_44",
                "gender": "MALE",
                "population": 108,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_45_49",
                "gender": "FEMALE",
                "population": 149,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_45_49",
                "gender": "MALE",
                "population": 88,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_50_54",
                "gender": "FEMALE",
                "population": 118,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_50_54",
                "gender": "MALE",
                "population": 88,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_55_59",
                "gender": "FEMALE",
                "population": 88,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_55_59",
                "gender": "MALE",
                "population": 58,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_5_9",
                "gender": "FEMALE",
                "population": 221,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_5_9",
                "gender": "MALE",
                "population": 180,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_60_64",
                "gender": "FEMALE",
                "population": 79,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_60_64",
                "gender": "MALE",
                "population": 78,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_65_69",
                "gender": "FEMALE",
                "population": 67,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_65_69",
                "gender": "MALE",
                "population": 43,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_70_74",
                "gender": "FEMALE",
                "population": 52,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_70_74",
                "gender": "MALE",
                "population": 43,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "FEMALE",
                "population": 86,
            },
            {
                "ward_number": 6,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "MALE",
                "population": 108,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_0_4",
                "gender": "FEMALE",
                "population": 78,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_0_4",
                "gender": "MALE",
                "population": 154,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_10_14",
                "gender": "FEMALE",
                "population": 138,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_10_14",
                "gender": "MALE",
                "population": 168,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_15_19",
                "gender": "FEMALE",
                "population": 166,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_15_19",
                "gender": "MALE",
                "population": 129,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_20_24",
                "gender": "FEMALE",
                "population": 136,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_20_24",
                "gender": "MALE",
                "population": 141,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_25_29",
                "gender": "FEMALE",
                "population": 108,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_25_29",
                "gender": "MALE",
                "population": 111,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_30_34",
                "gender": "FEMALE",
                "population": 108,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_30_34",
                "gender": "MALE",
                "population": 66,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_35_39",
                "gender": "FEMALE",
                "population": 100,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_35_39",
                "gender": "MALE",
                "population": 75,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_40_44",
                "gender": "FEMALE",
                "population": 79,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_40_44",
                "gender": "MALE",
                "population": 51,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_45_49",
                "gender": "FEMALE",
                "population": 79,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_45_49",
                "gender": "MALE",
                "population": 46,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_50_54",
                "gender": "FEMALE",
                "population": 49,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_50_54",
                "gender": "MALE",
                "population": 45,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_55_59",
                "gender": "FEMALE",
                "population": 48,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_55_59",
                "gender": "MALE",
                "population": 22,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_5_9",
                "gender": "FEMALE",
                "population": 112,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_5_9",
                "gender": "MALE",
                "population": 142,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_60_64",
                "gender": "FEMALE",
                "population": 45,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_60_64",
                "gender": "MALE",
                "population": 30,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_65_69",
                "gender": "FEMALE",
                "population": 35,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_65_69",
                "gender": "MALE",
                "population": 22,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_70_74",
                "gender": "FEMALE",
                "population": 36,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_70_74",
                "gender": "MALE",
                "population": 17,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "FEMALE",
                "population": 57,
            },
            {
                "ward_number": 7,
                "age_group": "AGE_75_AND_ABOVE",
                "gender": "MALE",
                "population": 20,
            },
        ]

        self.stdout.write(
            f"Processing {len(actual_data)} age-gender demographic records..."
        )

        existing_count = WardAgeWisePopulation.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        updated_count = 0
        with transaction.atomic():
            for data_item in actual_data:
                obj, created = WardAgeWisePopulation.objects.get_or_create(
                    ward_number=data_item["ward_number"],
                    age_group=data_item["age_group"],
                    gender=data_item["gender"],
                    defaults={
                        "id": str(uuid.uuid4()),
                        "population": data_item["population"],
                    },
                )

                if created:
                    created_count += 1
                else:
                    obj.population = data_item["population"]
                    obj.save()
                    updated_count += 1

        # Calculate and display summary statistics
        total_records = WardAgeWisePopulation.objects.count()
        total_population = sum(
            WardAgeWisePopulation.objects.values_list("population", flat=True)
        )

        total_male = sum(
            WardAgeWisePopulation.objects.filter(gender="MALE").values_list(
                "population", flat=True
            )
        )

        total_female = sum(
            WardAgeWisePopulation.objects.filter(gender="FEMALE").values_list(
                "population", flat=True
            )
        )

        total_other = sum(
            WardAgeWisePopulation.objects.filter(gender="OTHER").values_list(
                "population", flat=True
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(actual_data)} age-gender demographic records "
                f"({created_count} new, {updated_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people\n"
                f"Male: {total_male:,} ({total_male/total_population*100:.1f}%)\n"
                f"Female: {total_female:,} ({total_female/total_population*100:.1f}%)\n"
                f"Other: {total_other:,} ({total_other/total_population*100:.1f}%)"
            )
        )

        # Display breakdown by age groups
        self.stdout.write("\nAge group breakdown:")
        for age_choice in AgeGroupChoice.choices:
            age_code = age_choice[0]
            age_name = age_choice[1]
            age_total = sum(
                WardAgeWisePopulation.objects.filter(age_group=age_code).values_list(
                    "population", flat=True
                )
            )
            age_male = sum(
                WardAgeWisePopulation.objects.filter(
                    age_group=age_code, gender="MALE"
                ).values_list("population", flat=True)
            )
            age_female = sum(
                WardAgeWisePopulation.objects.filter(
                    age_group=age_code, gender="FEMALE"
                ).values_list("population", flat=True)
            )

            if age_total > 0:
                percentage = age_total / total_population * 100
                self.stdout.write(
                    f"  {age_name}: {age_total:,} total ({percentage:.1f}%) - "
                    f"Male: {age_male:,}, Female: {age_female:,}"
                )

        # Display ward breakdown
        self.stdout.write("\nWard breakdown:")
        for ward_num in range(1, 8):
            ward_total = sum(
                WardAgeWisePopulation.objects.filter(ward_number=ward_num).values_list(
                    "population", flat=True
                )
            )
            ward_male = sum(
                WardAgeWisePopulation.objects.filter(
                    ward_number=ward_num, gender="MALE"
                ).values_list("population", flat=True)
            )
            ward_female = sum(
                WardAgeWisePopulation.objects.filter(
                    ward_number=ward_num, gender="FEMALE"
                ).values_list("population", flat=True)
            )

            if ward_total > 0:
                percentage = ward_total / total_population * 100
                self.stdout.write(
                    f"  Ward {ward_num}: {ward_total:,} total ({percentage:.1f}%) - "
                    f"Male: {ward_male:,}, Female: {ward_female:,}"
                )
