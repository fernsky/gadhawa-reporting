"""
Management command to create female property ownership demographics data based on latest actual data (wards 1-8, all property types)
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demographics.models import WardWiseFemalePropertyOwnership
import uuid


class Command(BaseCommand):
    help = "Create female property ownership demographics data based on latest actual municipality-wide data (wards 1-8, all property types)"

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
            "Creating female property ownership demographics data based on latest actual municipality-wide data (wards 1-8, all property types)..."
        )

        # Latest data from provided JSON (wards 1-8, all property types)
        female_property_data = [
            {
                "id": "43725587-539f-42ad-8996-de26bacbef95",
                "ward_number": 1,
                "property_type": "HOUSE_ONLY",
                "count": 24,
                "population": 24,
            },
            {
                "id": "4a3d55af-89c4-461f-bc11-bfbf447f0c95",
                "ward_number": 1,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 1449,
                "population": 1449,
            },
            {
                "id": "13802f45-bd48-46e1-84d9-b6eed94d16a1",
                "ward_number": 1,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 197,
                "population": 197,
            },
            {
                "id": "677b5f5b-34b6-4a20-99cd-1e0c6b48de4b",
                "ward_number": 1,
                "property_type": "LAND_ONLY",
                "count": 65,
                "population": 65,
            },
            {
                "id": "8a32dc9f-25f2-4451-911d-3b27be95e3ae",
                "ward_number": 2,
                "property_type": "HOUSE_ONLY",
                "count": 4,
                "population": 4,
            },
            {
                "id": "a00fe7f0-4ea8-4af0-9f01-d908d7fb64d9",
                "ward_number": 2,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 1030,
                "population": 1030,
            },
            {
                "id": "1c94f3bb-4f25-408c-892e-03d8b368fcf6",
                "ward_number": 2,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 64,
                "population": 64,
            },
            {
                "id": "82c2664a-2920-41ec-ae1a-502a6e52433b",
                "ward_number": 2,
                "property_type": "LAND_ONLY",
                "count": 103,
                "population": 103,
            },
            {
                "id": "6a92d20a-72f6-40f5-b470-1ad8c1c8ce53",
                "ward_number": 3,
                "property_type": "HOUSE_ONLY",
                "count": 15,
                "population": 15,
            },
            {
                "id": "921cd5d3-d2a4-4b26-8135-c803423d87b0",
                "ward_number": 3,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 1027,
                "population": 1027,
            },
            {
                "id": "a4e10617-413f-4831-ab12-c002a445f2dc",
                "ward_number": 3,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 156,
                "population": 156,
            },
            {
                "id": "9e5255fe-2d2d-41e1-a24c-a558e8e4a796",
                "ward_number": 3,
                "property_type": "LAND_ONLY",
                "count": 96,
                "population": 96,
            },
            {
                "id": "12435944-6e1c-44e5-b174-2be94606ccf2",
                "ward_number": 4,
                "property_type": "HOUSE_ONLY",
                "count": 4,
                "population": 4,
            },
            {
                "id": "82c3346d-32f2-4c02-b74c-1ec346fbb1e5",
                "ward_number": 4,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 996,
                "population": 996,
            },
            {
                "id": "76880892-5899-4497-8cbf-9b46f4bfac94",
                "ward_number": 4,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 189,
                "population": 189,
            },
            {
                "id": "9f7dae95-25dd-49de-a3f2-34b0760c2d09",
                "ward_number": 4,
                "property_type": "LAND_ONLY",
                "count": 111,
                "population": 111,
            },
            {
                "id": "85a464eb-2858-40b3-9a40-a9af1e36c244",
                "ward_number": 5,
                "property_type": "HOUSE_ONLY",
                "count": 25,
                "population": 25,
            },
            {
                "id": "45eb908d-eb16-449e-9e71-a7a759ce6727",
                "ward_number": 5,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 1186,
                "population": 1186,
            },
            {
                "id": "af2cf948-9c32-4129-ad7f-2af6f06b8d18",
                "ward_number": 5,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 160,
                "population": 160,
            },
            {
                "id": "88f05ea8-9d76-4bdc-adbc-fc736fdcc905",
                "ward_number": 5,
                "property_type": "LAND_ONLY",
                "count": 151,
                "population": 151,
            },
            {
                "id": "740ff9e6-3a1b-4953-9bca-65eb25dc161f",
                "ward_number": 6,
                "property_type": "HOUSE_ONLY",
                "count": 34,
                "population": 34,
            },
            {
                "id": "5f2f4b2b-b6ad-4125-bf4b-8706bbbe7aae",
                "ward_number": 6,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 1238,
                "population": 1238,
            },
            {
                "id": "c3a57f3e-24f9-4006-ab18-90e0d0312f33",
                "ward_number": 6,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 217,
                "population": 217,
            },
            {
                "id": "1e8b244d-b92a-4d25-807d-8d42f19fc35e",
                "ward_number": 6,
                "property_type": "LAND_ONLY",
                "count": 272,
                "population": 272,
            },
            {
                "id": "46f05ff2-bf5d-4b46-841b-3a1e1db5529c",
                "ward_number": 7,
                "property_type": "HOUSE_ONLY",
                "count": 28,
                "population": 28,
            },
            {
                "id": "f64e0e11-742e-48b8-a0c9-04f0609b7c92",
                "ward_number": 7,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 959,
                "population": 959,
            },
            {
                "id": "a6168d6c-3bfb-4a34-bfdb-780c1c71de10",
                "ward_number": 7,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 154,
                "population": 154,
            },
            {
                "id": "04480f0d-d815-4a46-9c0f-18f8f79663f8",
                "ward_number": 7,
                "property_type": "LAND_ONLY",
                "count": 216,
                "population": 216,
            },
            {
                "id": "86a5d97a-2730-41e7-af6b-f05d2fa2e508",
                "ward_number": 8,
                "property_type": "NEITHER_HOUSE_NOR_LAND",
                "count": 189,
                "population": 189,
            },
            {
                "id": "89e5b814-b469-4c40-b124-a89488bc4985",
                "ward_number": 8,
                "property_type": "BOTH_HOUSE_AND_LAND",
                "count": 4,
                "population": 4,
            },
            {
                "id": "6785b649-aa21-43bd-a62b-1a87d7fe2389",
                "ward_number": 8,
                "property_type": "LAND_ONLY",
                "count": 3,
                "population": 3,
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
                percentage = (
                    property_total / total_population * 100
                    if total_population > 0
                    else 0
                )
                self.stdout.write(
                    f"  {property_name}: {property_total:,} people ({percentage:.1f}%)"
                )

        # Display ward breakdown
        self.stdout.write("\nWard breakdown:")
        for ward_num in range(1, 9):  # Now covering wards 1-8
            ward_total = sum(
                WardWiseFemalePropertyOwnership.objects.filter(
                    ward_number=ward_num
                ).values_list("population", flat=True)
            )

            if ward_total > 0:
                percentage = (
                    ward_total / total_population * 100 if total_population > 0 else 0
                )
                self.stdout.write(
                    f"  वडा {ward_num}: {ward_total:,} people ({percentage:.1f}%)"
                )
