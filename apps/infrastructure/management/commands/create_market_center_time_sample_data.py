"""
Management command to create market center time infrastructure data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.infrastructure.models import WardWiseTimeToMarketCenter, TimeDurationChoice
import uuid


class Command(BaseCommand):
    help = "Create market center time infrastructure data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing market center time data...")
            )
            WardWiseTimeToMarketCenter.objects.all().delete()

        self.stdout.write(
            "Creating market center time infrastructure data based on actual municipality-wide data..."
        )

        # Sample data representing actual market center accessibility patterns by ward
        market_center_time_data = [
            {
                "id": "a65613d6-0846-490f-978c-d468bf507959",
                "ward_number": 1,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 224,
            },
            {
                "id": "8a804970-b7d3-4591-ae0d-5c03cc3cf761",
                "ward_number": 1,
                "time_duration": "UNDER_15_MIN",
                "households": 277,
            },
            {
                "id": "bb3dfcda-97a3-4736-b198-c34403e18aff",
                "ward_number": 1,
                "time_duration": "UNDER_1_HOUR",
                "households": 395,
            },
            {
                "id": "ac556f1e-a87d-4cbf-8afd-0b0a5e16bf0e",
                "ward_number": 1,
                "time_duration": "UNDER_30_MIN",
                "households": 839,
            },
            {
                "id": "9b953a6a-3b79-4045-aa4c-4140ab4419a6",
                "ward_number": 2,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 76,
            },
            {
                "id": "c8468ca8-d2fe-4ba0-a8b2-4745413dc900",
                "ward_number": 2,
                "time_duration": "UNDER_15_MIN",
                "households": 580,
            },
            {
                "id": "77183b2e-19dd-492a-a71f-09abbfaf055e",
                "ward_number": 2,
                "time_duration": "UNDER_1_HOUR",
                "households": 175,
            },
            {
                "id": "192702dd-d23d-46da-b84d-81e48d4e45df",
                "ward_number": 2,
                "time_duration": "UNDER_30_MIN",
                "households": 370,
            },
            {
                "id": "e5a1cfc7-9266-4ceb-b352-9f27c33cb90e",
                "ward_number": 3,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 157,
            },
            {
                "id": "19c5ac20-6e47-470f-a04b-39dc983ef47c",
                "ward_number": 3,
                "time_duration": "UNDER_15_MIN",
                "households": 454,
            },
            {
                "id": "6db17a40-2768-461f-a6c4-bc5ee07e17e9",
                "ward_number": 3,
                "time_duration": "UNDER_1_HOUR",
                "households": 220,
            },
            {
                "id": "0ff5e693-c56a-4bcc-b095-4bbf03197788",
                "ward_number": 3,
                "time_duration": "UNDER_30_MIN",
                "households": 463,
            },
            {
                "id": "d57df96c-3252-4470-b74a-00d6b831ceda",
                "ward_number": 4,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 301,
            },
            {
                "id": "85a6f574-77de-4ade-9a54-2904162cfa0a",
                "ward_number": 4,
                "time_duration": "UNDER_15_MIN",
                "households": 405,
            },
            {
                "id": "19c7cb65-b9e3-4afb-9e76-d2e7f673e655",
                "ward_number": 4,
                "time_duration": "UNDER_1_HOUR",
                "households": 221,
            },
            {
                "id": "af80ab17-752e-4051-b2ff-94649d2aba80",
                "ward_number": 4,
                "time_duration": "UNDER_30_MIN",
                "households": 373,
            },
            {
                "id": "1fc5bac0-c572-4aff-932e-58d45cf3f0ff",
                "ward_number": 5,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 342,
            },
            {
                "id": "02698828-a5ac-4857-9d2e-d1ad7bfb26c2",
                "ward_number": 5,
                "time_duration": "UNDER_15_MIN",
                "households": 118,
            },
            {
                "id": "239d7af9-e37f-4916-9f65-01aaa30ce75e",
                "ward_number": 5,
                "time_duration": "UNDER_1_HOUR",
                "households": 510,
            },
            {
                "id": "b98360d7-d868-461a-96ab-75ceedb6bd11",
                "ward_number": 5,
                "time_duration": "UNDER_30_MIN",
                "households": 552,
            },
            {
                "id": "dabb207f-2499-4c05-8398-a56ca89fede0",
                "ward_number": 6,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 121,
            },
            {
                "id": "55ccc71f-096d-440a-8c56-6aa106bdc106",
                "ward_number": 6,
                "time_duration": "UNDER_15_MIN",
                "households": 541,
            },
            {
                "id": "a0c70d72-da30-4fdf-9caa-9fa2db0ad3c6",
                "ward_number": 6,
                "time_duration": "UNDER_1_HOUR",
                "households": 407,
            },
            {
                "id": "5ecb7088-9da2-4fee-ae9d-6d3ce653fd67",
                "ward_number": 6,
                "time_duration": "UNDER_30_MIN",
                "households": 692,
            },
            {
                "id": "90b3123e-0ff6-46ec-b4dd-73e2be6db3d3",
                "ward_number": 7,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 10,
            },
            {
                "id": "b3bfe43c-f52a-4bc1-950d-faf603056026",
                "ward_number": 7,
                "time_duration": "UNDER_15_MIN",
                "households": 302,
            },
            {
                "id": "326feb62-6627-4671-bcbf-bc82f020499b",
                "ward_number": 7,
                "time_duration": "UNDER_1_HOUR",
                "households": 117,
            },
            {
                "id": "0d87f2dc-2954-4989-bbf7-ed0bd948ee2b",
                "ward_number": 7,
                "time_duration": "UNDER_30_MIN",
                "households": 928,
            },
            {
                "id": "32d8fe82-f53d-4b3d-925d-32ec81a00dc6",
                "ward_number": 8,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 32,
            },
            {
                "id": "8ad6c1bc-d2ae-4493-9c90-db3ea7f88ce5",
                "ward_number": 8,
                "time_duration": "UNDER_15_MIN",
                "households": 62,
            },
            {
                "id": "bf422364-44ef-4dcf-bb79-1f2b1eb5fe0a",
                "ward_number": 8,
                "time_duration": "UNDER_1_HOUR",
                "households": 33,
            },
            {
                "id": "b3aef770-7210-4e34-8866-8b8b654b5cf2",
                "ward_number": 8,
                "time_duration": "UNDER_30_MIN",
                "households": 69,
            },
        ]

        # Check if data already exists
        existing_count = WardWiseTimeToMarketCenter.objects.count()
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
            for data in market_center_time_data:
                obj, created = WardWiseTimeToMarketCenter.objects.get_or_create(
                    ward_number=data["ward_number"],
                    time_duration=data["time_duration"],
                    defaults={
                        "id": data["id"],
                        "households": data["households"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['time_duration']} ({data['households']} households)"
                    )
                else:
                    # Update existing record
                    obj.households = data["households"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['time_duration']} ({data['households']} households)"
                    )

        # Print summary
        total_records = WardWiseTimeToMarketCenter.objects.count()
        total_households = sum(
            WardWiseTimeToMarketCenter.objects.values_list("households", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(market_center_time_data)} market center time infrastructure records "
                f"({created_count} new, {len(market_center_time_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total households covered: {total_households:,} households"
            )
        )

        # Print time duration breakdown
        self.stdout.write("\nMarket center access time breakdown:")
        for time_choice in TimeDurationChoice.choices:
            time_code = time_choice[0]
            time_name = time_choice[1]
            time_households = (
                WardWiseTimeToMarketCenter.objects.filter(
                    time_duration=time_code
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )

            if time_households > 0:
                percentage = time_households / total_households * 100
                self.stdout.write(
                    f"  {time_name}: {time_households:,} households ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {time_name}: 0 households (0.00%)")

        # Accessibility analysis
        self.stdout.write("\nAccessibility Analysis:")
        excellent_access = (
            WardWiseTimeToMarketCenter.objects.filter(
                time_duration="UNDER_15_MIN"
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
        )
        good_access = (
            WardWiseTimeToMarketCenter.objects.filter(
                time_duration="UNDER_30_MIN"
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
        )

        good_accessibility = excellent_access + good_access
        good_percentage = (
            (good_accessibility / total_households * 100) if total_households > 0 else 0
        )

        self.stdout.write(
            f"  Excellent Access (< 15 min): {excellent_access:,} households"
        )
        self.stdout.write(
            f"  Good Access (< 30 min total): {good_accessibility:,} households ({good_percentage:.1f}%)"
        )

        # Ward-wise summary
        self.stdout.write("\nWard-wise market center accessibility summary:")
        for ward_num in range(1, 9):
            ward_households = (
                WardWiseTimeToMarketCenter.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )
            if ward_households > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_households:,} households")
