"""
Management command to create toilet type social data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.social.models import WardWiseToiletType, ToiletTypeChoice
import uuid


class Command(BaseCommand):
    help = "Create toilet type social data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing toilet type data...")
            )
            WardWiseToiletType.objects.all().delete()

        self.stdout.write(
            "Creating toilet type social data based on actual municipality-wide data..."
        )

        # Updated sample data representing actual toilet type patterns by ward (including ward 8)
        toilet_type_data = [
            {
                "id": "a6ad6020-5ed0-4608-8079-f706bac5c9da",
                "ward_number": 1,
                "toilet_type": "FLUSH_WITH_SEPTIC_TANK",
                "households": 181,
            },
            {
                "id": "83e06e4d-dffc-4b7c-997b-93d68580b831",
                "ward_number": 1,
                "toilet_type": "NORMAL",
                "households": 1468,
            },
            {
                "id": "ef1e62f4-09c7-4893-81f4-23c743cd8446",
                "ward_number": 1,
                "toilet_type": "NO_TOILET",
                "households": 33,
            },
            {
                "id": "02cefaa0-ecd2-48bc-aa33-624fe1ed80ff",
                "ward_number": 1,
                "toilet_type": "PUBLIC_EILANI",
                "households": 53,
            },
            {
                "id": "b96115f3-4bb4-4c52-ac09-a7947da8066b",
                "ward_number": 2,
                "toilet_type": "FLUSH_WITH_SEPTIC_TANK",
                "households": 146,
            },
            {
                "id": "9ba182df-d42e-46a4-95ea-436518fa7045",
                "ward_number": 2,
                "toilet_type": "NORMAL",
                "households": 1015,
            },
            {
                "id": "ca1234dd-3a51-4a0e-8351-292d9a495f7c",
                "ward_number": 2,
                "toilet_type": "NO_TOILET",
                "households": 31,
            },
            {
                "id": "e36bf908-a0a6-442a-b990-51ecb768c9ed",
                "ward_number": 2,
                "toilet_type": "PUBLIC_EILANI",
                "households": 9,
            },
            {
                "id": "a215fa03-4ff2-44dd-a422-795755c78faa",
                "ward_number": 3,
                "toilet_type": "FLUSH_WITH_SEPTIC_TANK",
                "households": 634,
            },
            {
                "id": "e07791e3-c3ba-45e9-836c-c5bb3ee52317",
                "ward_number": 3,
                "toilet_type": "NORMAL",
                "households": 621,
            },
            {
                "id": "069e944b-f764-4efd-bcad-1402f16bfcb2",
                "ward_number": 3,
                "toilet_type": "NO_TOILET",
                "households": 32,
            },
            {
                "id": "babdafbf-2025-415b-a1bd-e666621388ff",
                "ward_number": 3,
                "toilet_type": "PUBLIC_EILANI",
                "households": 7,
            },
            {
                "id": "d2a5d2fb-2de6-4a5b-9f8e-7de9dd579721",
                "ward_number": 4,
                "toilet_type": "FLUSH_WITH_SEPTIC_TANK",
                "households": 379,
            },
            {
                "id": "e8aac6be-ca55-468d-9849-8db0327685d8",
                "ward_number": 4,
                "toilet_type": "NORMAL",
                "households": 870,
            },
            {
                "id": "175910d8-a3fd-4d00-9f40-ec18127509fe",
                "ward_number": 4,
                "toilet_type": "NO_TOILET",
                "households": 51,
            },
            {
                "id": "8af1f2fe-ffe7-4081-a538-939b0995e811",
                "ward_number": 5,
                "toilet_type": "FLUSH_WITH_SEPTIC_TANK",
                "households": 505,
            },
            {
                "id": "ae800f8f-7600-4ff7-b10a-9e809af7d84c",
                "ward_number": 5,
                "toilet_type": "NORMAL",
                "households": 936,
            },
            {
                "id": "132b37b1-bbbe-436b-83d0-ee22906450b2",
                "ward_number": 5,
                "toilet_type": "NO_TOILET",
                "households": 66,
            },
            {
                "id": "e0ed08d7-f199-4e47-a8e5-bc936584d6d5",
                "ward_number": 5,
                "toilet_type": "PUBLIC_EILANI",
                "households": 15,
            },
            {
                "id": "20d3df0c-3b3c-45f1-9397-92c5d547d1bc",
                "ward_number": 6,
                "toilet_type": "FLUSH_WITH_SEPTIC_TANK",
                "households": 178,
            },
            {
                "id": "da62b48d-28b2-406a-935c-63b792e240b9",
                "ward_number": 6,
                "toilet_type": "NORMAL",
                "households": 1454,
            },
            {
                "id": "94e6a342-dae9-4846-832a-dd36d23cd57f",
                "ward_number": 6,
                "toilet_type": "NO_TOILET",
                "households": 126,
            },
            {
                "id": "12bac4a1-7619-4203-8231-4c66d16742ee",
                "ward_number": 6,
                "toilet_type": "PUBLIC_EILANI",
                "households": 3,
            },
            {
                "id": "089db645-6ae5-48d1-88a3-37f9e44ddd35",
                "ward_number": 7,
                "toilet_type": "FLUSH_WITH_SEPTIC_TANK",
                "households": 581,
            },
            {
                "id": "ba06a2c2-e646-45fc-a31e-8d6c1a23865f",
                "ward_number": 7,
                "toilet_type": "NORMAL",
                "households": 740,
            },
            {
                "id": "218006ee-8fa8-4bc0-9985-b42c5b318360",
                "ward_number": 7,
                "toilet_type": "NO_TOILET",
                "households": 34,
            },
            {
                "id": "1a03128e-06bf-482c-860e-e5c850e09463",
                "ward_number": 7,
                "toilet_type": "PUBLIC_EILANI",
                "households": 2,
            },
            {
                "id": "3a44309e-a320-4a07-a91f-6a7b4550cbb2",
                "ward_number": 8,
                "toilet_type": "FLUSH_WITH_SEPTIC_TANK",
                "households": 180,
            },
            {
                "id": "ce9bbc7c-4376-45a5-9b32-cc57df0b9897",
                "ward_number": 8,
                "toilet_type": "NORMAL",
                "households": 9,
            },
            {
                "id": "e4cef1e7-5393-4e1e-9ad9-38006fe784d4",
                "ward_number": 8,
                "toilet_type": "NO_TOILET",
                "households": 7,
            },
        ]

        # Check if data already exists
        existing_count = WardWiseToiletType.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        # Create records using Django ORM
        created_count = 0
        with transaction.atomic():
            for data in toilet_type_data:
                obj, created = WardWiseToiletType.objects.get_or_create(
                    ward_number=data["ward_number"],
                    toilet_type=data["toilet_type"],
                    defaults={
                        "id": data["id"],
                        "households": data["households"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['toilet_type']} ({data['households']} households)"
                    )
                else:
                    # Update existing record
                    obj.households = data["households"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['toilet_type']} ({data['households']} households)"
                    )

        # Print summary
        total_records = WardWiseToiletType.objects.count()
        total_households = sum(
            WardWiseToiletType.objects.values_list("households", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(toilet_type_data)} toilet type social records "
                f"({created_count} new, {len(toilet_type_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total households covered: {total_households:,} households"
            )
        )

        # Print toilet type breakdown
        self.stdout.write("\nToilet type breakdown:")
        for toilet_choice in ToiletTypeChoice.choices:
            toilet_code = toilet_choice[0]
            toilet_name = toilet_choice[1]
            toilet_households = (
                WardWiseToiletType.objects.filter(toilet_type=toilet_code).aggregate(
                    total=models.Sum("households")
                )["total"]
                or 0
            )

            if toilet_households > 0:
                percentage = toilet_households / total_households * 100
                self.stdout.write(
                    f"  {toilet_name}: {toilet_households:,} households ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {toilet_name}: 0 households (0.00%)")

        # Ward-wise summary (now for 8 wards)
        self.stdout.write("\nWard-wise toilet summary:")
        for ward_num in range(1, 9):
            ward_households = (
                WardWiseToiletType.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("households")
                )["total"]
                or 0
            )
            if ward_households > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_households:,} households")
