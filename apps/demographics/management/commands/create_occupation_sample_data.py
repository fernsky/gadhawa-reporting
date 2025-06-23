"""
Management command to create occupation demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.demographics.models import WardWiseMajorOccupation
import uuid


class Command(BaseCommand):
    help = "Create occupation demographics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing occupation data...")
            )
            WardWiseMajorOccupation.objects.all().delete()

        self.stdout.write(
            "Creating occupation demographics data based on actual municipality-wide data..."
        )

        # Updated sample data from user (8 wards, new occupation codes)
        occupation_data = [
            {"ward_number": 1, "occupation": "animal_husbandry", "population": 238},
            {"ward_number": 1, "occupation": "business", "population": 188},
            {"ward_number": 1, "occupation": "foreign_employment", "population": 908},
            {"ward_number": 1, "occupation": "governmental_job", "population": 78},
            {"ward_number": 1, "occupation": "householder", "population": 174},
            {"ward_number": 1, "occupation": "industry", "population": 209},
            {"ward_number": 1, "occupation": "labour", "population": 1045},
            {"ward_number": 1, "occupation": "non_governmental_job", "population": 151},
            {"ward_number": 1, "occupation": "other", "population": 100},
            {
                "ward_number": 1,
                "occupation": "other_self_employment",
                "population": 333,
            },
            {"ward_number": 1, "occupation": "other_unemployment", "population": 48},
            {"ward_number": 1, "occupation": "student", "population": 271},
            {"ward_number": 2, "occupation": "animal_husbandry", "population": 99},
            {"ward_number": 2, "occupation": "business", "population": 164},
            {"ward_number": 2, "occupation": "foreign_employment", "population": 269},
            {"ward_number": 2, "occupation": "governmental_job", "population": 115},
            {"ward_number": 2, "occupation": "householder", "population": 305},
            {"ward_number": 2, "occupation": "industry", "population": 92},
            {"ward_number": 2, "occupation": "labour", "population": 1156},
            {"ward_number": 2, "occupation": "non_governmental_job", "population": 95},
            {"ward_number": 2, "occupation": "other", "population": 77},
            {"ward_number": 2, "occupation": "other_self_employment", "population": 26},
            {"ward_number": 2, "occupation": "other_unemployment", "population": 8},
            {"ward_number": 2, "occupation": "student", "population": 12},
            {"ward_number": 3, "occupation": "animal_husbandry", "population": 90},
            {"ward_number": 3, "occupation": "business", "population": 138},
            {"ward_number": 3, "occupation": "foreign_employment", "population": 418},
            {"ward_number": 3, "occupation": "governmental_job", "population": 129},
            {"ward_number": 3, "occupation": "householder", "population": 441},
            {"ward_number": 3, "occupation": "industry", "population": 63},
            {"ward_number": 3, "occupation": "labour", "population": 1082},
            {"ward_number": 3, "occupation": "non_governmental_job", "population": 92},
            {"ward_number": 3, "occupation": "other", "population": 183},
            {"ward_number": 3, "occupation": "other_self_employment", "population": 73},
            {"ward_number": 3, "occupation": "other_unemployment", "population": 11},
            {"ward_number": 3, "occupation": "student", "population": 201},
            {"ward_number": 4, "occupation": "animal_husbandry", "population": 76},
            {"ward_number": 4, "occupation": "business", "population": 175},
            {"ward_number": 4, "occupation": "foreign_employment", "population": 533},
            {"ward_number": 4, "occupation": "governmental_job", "population": 180},
            {"ward_number": 4, "occupation": "householder", "population": 707},
            {"ward_number": 4, "occupation": "industry", "population": 515},
            {"ward_number": 4, "occupation": "labour", "population": 909},
            {"ward_number": 4, "occupation": "non_governmental_job", "population": 73},
            {"ward_number": 4, "occupation": "other", "population": 80},
            {"ward_number": 4, "occupation": "other_self_employment", "population": 73},
            {"ward_number": 4, "occupation": "other_unemployment", "population": 17},
            {"ward_number": 4, "occupation": "student", "population": 432},
            {"ward_number": 5, "occupation": "animal_husbandry", "population": 37},
            {"ward_number": 5, "occupation": "business", "population": 72},
            {"ward_number": 5, "occupation": "foreign_employment", "population": 359},
            {"ward_number": 5, "occupation": "governmental_job", "population": 121},
            {"ward_number": 5, "occupation": "householder", "population": 428},
            {"ward_number": 5, "occupation": "industry", "population": 174},
            {"ward_number": 5, "occupation": "labour", "population": 1238},
            {"ward_number": 5, "occupation": "non_governmental_job", "population": 209},
            {"ward_number": 5, "occupation": "other", "population": 73},
            {"ward_number": 5, "occupation": "other_self_employment", "population": 33},
            {"ward_number": 5, "occupation": "other_unemployment", "population": 112},
            {"ward_number": 5, "occupation": "student", "population": 32},
            {"ward_number": 6, "occupation": "animal_husbandry", "population": 93},
            {"ward_number": 6, "occupation": "business", "population": 242},
            {"ward_number": 6, "occupation": "foreign_employment", "population": 816},
            {"ward_number": 6, "occupation": "governmental_job", "population": 206},
            {"ward_number": 6, "occupation": "householder", "population": 1233},
            {"ward_number": 6, "occupation": "industry", "population": 154},
            {"ward_number": 6, "occupation": "labour", "population": 723},
            {"ward_number": 6, "occupation": "non_governmental_job", "population": 199},
            {"ward_number": 6, "occupation": "other", "population": 38},
            {"ward_number": 6, "occupation": "other_self_employment", "population": 55},
            {"ward_number": 6, "occupation": "other_unemployment", "population": 25},
            {"ward_number": 6, "occupation": "student", "population": 572},
            {"ward_number": 7, "occupation": "animal_husbandry", "population": 88},
            {"ward_number": 7, "occupation": "business", "population": 124},
            {"ward_number": 7, "occupation": "foreign_employment", "population": 477},
            {"ward_number": 7, "occupation": "governmental_job", "population": 106},
            {"ward_number": 7, "occupation": "householder", "population": 349},
            {"ward_number": 7, "occupation": "industry", "population": 898},
            {"ward_number": 7, "occupation": "labour", "population": 843},
            {"ward_number": 7, "occupation": "non_governmental_job", "population": 141},
            {"ward_number": 7, "occupation": "other", "population": 220},
            {"ward_number": 7, "occupation": "other_self_employment", "population": 46},
            {"ward_number": 7, "occupation": "other_unemployment", "population": 6},
            {"ward_number": 7, "occupation": "student", "population": 276},
            {"ward_number": 8, "occupation": "animal_husbandry", "population": 1},
            {"ward_number": 8, "occupation": "business", "population": 32},
            {"ward_number": 8, "occupation": "foreign_employment", "population": 97},
            {"ward_number": 8, "occupation": "governmental_job", "population": 5},
            {"ward_number": 8, "occupation": "householder", "population": 229},
            {"ward_number": 8, "occupation": "labour", "population": 114},
            {"ward_number": 8, "occupation": "non_governmental_job", "population": 25},
            {"ward_number": 8, "occupation": "other", "population": 9},
            {"ward_number": 8, "occupation": "other_self_employment", "population": 5},
            {"ward_number": 8, "occupation": "other_unemployment", "population": 16},
            {"ward_number": 8, "occupation": "student", "population": 174},
        ]

        # Assign UUIDs for each record
        import uuid

        for data in occupation_data:
            data["id"] = str(uuid.uuid4())

        existing_count = WardWiseMajorOccupation.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in occupation_data:
                obj, created = WardWiseMajorOccupation.objects.get_or_create(
                    ward_number=data["ward_number"],
                    occupation=data["occupation"],
                    defaults={
                        "id": data["id"],
                        "population": data["population"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['occupation']} ({data['population']} people)"
                    )
                else:
                    obj.population = data["population"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['occupation']} ({data['population']} people)"
                    )

        total_records = WardWiseMajorOccupation.objects.count()
        total_population = sum(
            WardWiseMajorOccupation.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(occupation_data)} occupation demographic records "
                f"({created_count} new, {len(occupation_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people"
            )
        )

        # Calculate and display occupation-wise summary
        self.stdout.write("\nOccupation-wise summary:")
        occupation_totals = {}
        occupation_codes = set([d["occupation"] for d in occupation_data])
        for occupation in occupation_codes:
            occupation_population = (
                WardWiseMajorOccupation.objects.filter(occupation=occupation).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            occupation_totals[occupation] = occupation_population
            if occupation_population > 0:
                percentage = occupation_population / total_population * 100
                self.stdout.write(
                    f"  {occupation}: {occupation_population:,} people ({percentage:.2f}%)"
                )

        # Ward-wise summary
        self.stdout.write("\nWard-wise occupation summary:")
        for ward_num in range(1, 9):  # Wards 1-8 based on data
            ward_population = (
                WardWiseMajorOccupation.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            if ward_population > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_population:,} people")
