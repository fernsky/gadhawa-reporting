"""
Management command to create female property ownership demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import WardWiseFemalePropertyOwnership
import uuid


class Command(BaseCommand):
    help = "Create female property ownership demographics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    "Clearing existing female property ownership data..."
                )
            )
            WardWiseFemalePropertyOwnership.objects.all().delete()

        self.stdout.write(
            "Creating female property ownership demographics data based on actual municipality-wide data..."
        )

        # Actual data from the provided JSON
        female_property_data = [
            {
                "id": "093ee6d0-e12c-400f-9abe-1c35cbbb5080",
                "ward_number": 1,
                "property_type": "HOUSE_ONLY",
                "count": 25,
                "population": 25,
            },
            {
                "id": "87a3dc41-c8fa-4854-acb0-d5653658ebbc",
                "ward_number": 1,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 999,
                "population": 999,
            },
            {
                "id": "65bcfb1d-eb09-4a36-8825-de41294f6e6f",
                "ward_number": 1,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 80,
                "population": 80,
            },
            {
                "id": "625982ed-db5c-489b-91e1-837ca2c1f908",
                "ward_number": 1,
                "property_type": "LAND_ONLY",
                "count": 35,
                "population": 35,
            },
            {
                "id": "4e716c83-7b71-4e0a-89f3-71e4f5bd9f9a",
                "ward_number": 2,
                "property_type": "HOUSE_ONLY",
                "count": 12,
                "population": 12,
            },
            {
                "id": "2d29da74-4ed1-49a6-99c5-e696c437ce28",
                "ward_number": 2,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 653,
                "population": 653,
            },
            {
                "id": "f7d51a64-c02e-415a-b70a-ffc18f1c2ce8",
                "ward_number": 2,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 185,
                "population": 185,
            },
            {
                "id": "36ca2047-2076-4ec8-ac9d-a7766bd83813",
                "ward_number": 2,
                "property_type": "LAND_ONLY",
                "count": 68,
                "population": 68,
            },
            {
                "id": "128ef8cd-3abb-48d9-99a0-2cc6955fbba7",
                "ward_number": 3,
                "property_type": "HOUSE_ONLY",
                "count": 10,
                "population": 10,
            },
            {
                "id": "4908e162-4a0b-4790-9b93-4b2f68725c4f",
                "ward_number": 3,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 534,
                "population": 534,
            },
            {
                "id": "d32dcd3c-6b88-47b4-b8a0-f7f0b44d7fd9",
                "ward_number": 3,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 8,
                "population": 8,
            },
            {
                "id": "bd4c370e-c1d7-46ec-bcff-78a945e624cb",
                "ward_number": 3,
                "property_type": "LAND_ONLY",
                "count": 12,
                "population": 12,
            },
            {
                "id": "ba2118c3-9855-4533-9a7e-58050cb5975c",
                "ward_number": 4,
                "property_type": "HOUSE_ONLY",
                "count": 3,
                "population": 3,
            },
            {
                "id": "329f883d-bcfb-4497-87b1-020418b0e804",
                "ward_number": 4,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 702,
                "population": 702,
            },
            {
                "id": "8f710890-28da-4cd1-a337-3e73e04ef331",
                "ward_number": 4,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 70,
                "population": 70,
            },
            {
                "id": "55481e97-e943-4493-9da9-1e2b2d75006b",
                "ward_number": 4,
                "property_type": "LAND_ONLY",
                "count": 73,
                "population": 73,
            },
            {
                "id": "81155404-dba2-4b02-aa10-8b880f2ad3cb",
                "ward_number": 5,
                "property_type": "HOUSE_ONLY",
                "count": 3,
                "population": 3,
            },
            {
                "id": "89127543-58d3-4f81-ae09-d1a3eadf0fee",
                "ward_number": 5,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 543,
                "population": 543,
            },
            {
                "id": "c8ba4db5-585b-4f8d-8763-eff47eae3266",
                "ward_number": 5,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 73,
                "population": 73,
            },
            {
                "id": "2b0a2049-ff1d-4e27-8b57-53c1f07a87a3",
                "ward_number": 5,
                "property_type": "LAND_ONLY",
                "count": 100,
                "population": 100,
            },
            {
                "id": "2c82a9a3-e76f-469e-acc8-bbb77f59d980",
                "ward_number": 6,
                "property_type": "HOUSE_ONLY",
                "count": 82,
                "population": 82,
            },
            {
                "id": "29fdb0ea-5bca-4d80-b702-696820de0c7c",
                "ward_number": 6,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 681,
                "population": 681,
            },
            {
                "id": "6ff833b4-aeec-4a52-a44f-7aa6b1f815f8",
                "ward_number": 6,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 67,
                "population": 67,
            },
            {
                "id": "0021c699-dd04-4d5a-bbfe-2b6b6d67d695",
                "ward_number": 6,
                "property_type": "LAND_ONLY",
                "count": 34,
                "population": 34,
            },
            {
                "id": "24dd55b4-707d-4a0f-a972-7ea9495702a5",
                "ward_number": 7,
                "property_type": "HOUSE_ONLY",
                "count": 5,
                "population": 5,
            },
            {
                "id": "27ef13b9-4be8-424c-87f3-e19efdc9ef37",
                "ward_number": 7,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 497,
                "population": 497,
            },
            {
                "id": "c16b59de-a312-4bce-8a35-961ccf33e16d",
                "ward_number": 7,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 78,
                "population": 78,
            },
            {
                "id": "6f1b18b6-4398-498b-853e-38ae77055de3",
                "ward_number": 7,
                "property_type": "LAND_ONLY",
                "count": 7,
                "population": 7,
            },
        ]

        self.stdout.write(
            f"Processing {len(female_property_data)} female property ownership records..."
        )

        existing_count = WardWiseFemalePropertyOwnership.objects.count()
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
            for data_item in female_property_data:
                obj, created = WardWiseFemalePropertyOwnership.objects.get_or_create(
                    ward_number=data_item["ward_number"],
                    property_type=data_item["property_type"],
                    defaults={
                        "id": data_item["id"],
                        "count": data_item["count"],
                        "population": data_item["population"],
                    },
                )

                if created:
                    created_count += 1
                else:
                    obj.count = data_item["count"]
                    obj.population = data_item["population"]
                    obj.save()
                    updated_count += 1

        # Calculate and display summary statistics
        total_records = WardWiseFemalePropertyOwnership.objects.count()
        total_population = sum(
            WardWiseFemalePropertyOwnership.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(female_property_data)} female property ownership records "
                f"({created_count} new, {updated_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total population covered: {total_population:,} people"
            )
        )

        # Display breakdown by property types
        self.stdout.write("\nProperty type breakdown:")
        from apps.demographics.models import PropertyTypeChoice

        for property_choice in PropertyTypeChoice.choices:
            property_code = property_choice[0]
            property_name = property_choice[1]
            property_total = sum(
                WardWiseFemalePropertyOwnership.objects.filter(
                    property_type=property_code
                ).values_list("population", flat=True)
            )

            if property_total > 0:
                percentage = property_total / total_population * 100
                self.stdout.write(
                    f"  {property_name}: {property_total:,} people ({percentage:.1f}%)"
                )

        # Display ward breakdown
        self.stdout.write("\nWard breakdown:")
        for ward_num in range(1, 8):  # Only wards 1-7 based on actual data
            ward_total = sum(
                WardWiseFemalePropertyOwnership.objects.filter(
                    ward_number=ward_num
                ).values_list("population", flat=True)
            )

            if ward_total > 0:
                percentage = ward_total / total_population * 100
                self.stdout.write(
                    f"  Ward {ward_num}: {ward_total:,} people ({percentage:.1f}%)"
                )
