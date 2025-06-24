"""
Management command to create public transport accessibility data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.infrastructure.models import WardWiseTimeToPublicTransport, TimeDurationChoice
import uuid


class Command(BaseCommand):
    help = "Create public transport accessibility data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing public transport data...")
            )
            WardWiseTimeToPublicTransport.objects.all().delete()

        self.stdout.write(
            "Creating public transport accessibility data based on actual municipality-wide data..."
        )

        # Sample data representing actual public transport accessibility patterns by ward and time duration
        public_transport_data = [
            {
                "id": "3ac504ee-829a-4f7c-902e-4dbe856066b2",
                "ward_number": 1,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 82,
            },
            {
                "id": "1510c717-2015-48c8-8bda-a81685588089",
                "ward_number": 1,
                "time_duration": "UNDER_15_MIN",
                "households": 549,
            },
            {
                "id": "d917ac06-e304-49e3-a3c5-1dd1c2c8b72f",
                "ward_number": 1,
                "time_duration": "UNDER_1_HOUR",
                "households": 287,
            },
            {
                "id": "671ab44c-35f5-4655-84f4-2990953cfbd9",
                "ward_number": 1,
                "time_duration": "UNDER_30_MIN",
                "households": 817,
            },
            {
                "id": "cf56c222-beb7-4981-9891-2056f3b5504c",
                "ward_number": 2,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 82,
            },
            {
                "id": "4b5c9fcd-81f0-451c-9a13-ef8f187aeb3d",
                "ward_number": 2,
                "time_duration": "UNDER_15_MIN",
                "households": 798,
            },
            {
                "id": "eb852c58-9c75-42f1-bc13-ea47f2f4548e",
                "ward_number": 2,
                "time_duration": "UNDER_1_HOUR",
                "households": 40,
            },
            {
                "id": "4866144a-6cfb-4657-81a0-80ae9506cdfc",
                "ward_number": 2,
                "time_duration": "UNDER_30_MIN",
                "households": 281,
            },
            {
                "id": "1a6ea3a3-36e8-4b5a-979c-9bdd0965d6ba",
                "ward_number": 3,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 11,
            },
            {
                "id": "a080d810-f4ec-47c3-93f1-893ae42c3016",
                "ward_number": 3,
                "time_duration": "UNDER_15_MIN",
                "households": 665,
            },
            {
                "id": "150452de-384e-4ddb-a3ac-04c53a91de88",
                "ward_number": 3,
                "time_duration": "UNDER_1_HOUR",
                "households": 178,
            },
            {
                "id": "47afc3a1-30be-447e-9483-d27f0ffb7db1",
                "ward_number": 3,
                "time_duration": "UNDER_30_MIN",
                "households": 440,
            },
            {
                "id": "b795aa12-cf17-422c-b9fd-f75f45d83ea4",
                "ward_number": 4,
                "time_duration": "UNDER_15_MIN",
                "households": 627,
            },
            {
                "id": "5feedfac-f8c9-47d8-88f2-e5a1405673cd",
                "ward_number": 4,
                "time_duration": "UNDER_1_HOUR",
                "households": 37,
            },
            {
                "id": "39dfefc4-9abe-41d0-be8f-7b9d92d7f316",
                "ward_number": 4,
                "time_duration": "UNDER_30_MIN",
                "households": 636,
            },
            {
                "id": "2b3b3215-2fcd-43de-8904-5cd248fae2f2",
                "ward_number": 5,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 11,
            },
            {
                "id": "da6b3c4f-976e-4ca9-bff8-6d15201e8803",
                "ward_number": 5,
                "time_duration": "UNDER_15_MIN",
                "households": 780,
            },
            {
                "id": "cb39fcfb-251a-4de7-b2c8-fff6fd79815a",
                "ward_number": 5,
                "time_duration": "UNDER_1_HOUR",
                "households": 50,
            },
            {
                "id": "63cf17f1-3a44-4d9c-a9b6-6d2d6c763a16",
                "ward_number": 5,
                "time_duration": "UNDER_30_MIN",
                "households": 681,
            },
            {
                "id": "de67a868-5649-48ca-8e25-f9f59071fff5",
                "ward_number": 6,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 92,
            },
            {
                "id": "34149c4b-80f9-4ee7-a013-96fcfc253f53",
                "ward_number": 6,
                "time_duration": "UNDER_15_MIN",
                "households": 937,
            },
            {
                "id": "64728ae5-62cf-4eac-af84-be144fd8d1dc",
                "ward_number": 6,
                "time_duration": "UNDER_1_HOUR",
                "households": 176,
            },
            {
                "id": "14ed0185-4fc1-4d8f-bf9f-e71044be47a3",
                "ward_number": 6,
                "time_duration": "UNDER_30_MIN",
                "households": 556,
            },
            {
                "id": "42709682-f65b-4085-9581-521ff3226581",
                "ward_number": 7,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 3,
            },
            {
                "id": "a635ccdc-73c7-4f98-9731-f75a33c6a46f",
                "ward_number": 7,
                "time_duration": "UNDER_15_MIN",
                "households": 357,
            },
            {
                "id": "728b8d4a-df57-49cf-a099-e0ba9290760d",
                "ward_number": 7,
                "time_duration": "UNDER_1_HOUR",
                "households": 94,
            },
            {
                "id": "853f9361-8793-4d28-830f-a368822a770c",
                "ward_number": 7,
                "time_duration": "UNDER_30_MIN",
                "households": 903,
            },
            {
                "id": "4c377433-a703-45b4-9006-7f4229816cbe",
                "ward_number": 8,
                "time_duration": "1_HOUR_OR_MORE",
                "households": 31,
            },
            {
                "id": "84d8a8ad-baba-446d-85ef-cda9397fb08f",
                "ward_number": 8,
                "time_duration": "UNDER_15_MIN",
                "households": 63,
            },
            {
                "id": "40da2b60-b0cd-4c37-b729-b2a1a811ffd7",
                "ward_number": 8,
                "time_duration": "UNDER_1_HOUR",
                "households": 33,
            },
            {
                "id": "d10ba189-c718-4609-a23f-da4ca2c76b7e",
                "ward_number": 8,
                "time_duration": "UNDER_30_MIN",
                "households": 69,
            },
        ]

        # Check if data already exists
        existing_count = WardWiseTimeToPublicTransport.objects.count()
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
            for data in public_transport_data:
                obj, created = WardWiseTimeToPublicTransport.objects.get_or_create(
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
        total_records = WardWiseTimeToPublicTransport.objects.count()
        total_households = sum(
            WardWiseTimeToPublicTransport.objects.values_list("households", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(public_transport_data)} public transport accessibility records "
                f"({created_count} new, {len(public_transport_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total households covered: {total_households:,} households"
            )
        )

        # Print time duration breakdown
        self.stdout.write("\nTime duration breakdown:")
        for time_choice in TimeDurationChoice.choices:
            time_code = time_choice[0]
            time_name = time_choice[1]
            time_households = (
                WardWiseTimeToPublicTransport.objects.filter(
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

        # Ward-wise summary
        self.stdout.write("\nWard-wise public transport accessibility summary:")
        for ward_num in range(1, 9):
            ward_households = (
                WardWiseTimeToPublicTransport.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )
            if ward_households > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_households:,} households")

        # Accessibility analysis
        excellent_access = (
            WardWiseTimeToPublicTransport.objects.filter(
                time_duration="UNDER_15_MIN"
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
        )
        good_access = (
            WardWiseTimeToPublicTransport.objects.filter(
                time_duration="UNDER_30_MIN"
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
        )
        poor_access = (
            WardWiseTimeToPublicTransport.objects.filter(
                time_duration="1_HOUR_OR_MORE"
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
        )

        combined_good_access = excellent_access + good_access
        good_access_percentage = (
            (combined_good_access / total_households * 100)
            if total_households > 0
            else 0
        )
        poor_access_percentage = (
            (poor_access / total_households * 100) if total_households > 0 else 0
        )

        self.stdout.write("\nAccessibility Analysis:")
        self.stdout.write(
            f"  Excellent access (under 15 min): {excellent_access:,} households"
        )
        self.stdout.write(
            f"  Good access (under 30 min total): {combined_good_access:,} households ({good_access_percentage:.1f}%)"
        )
        self.stdout.write(
            f"  Poor access (1 hour or more): {poor_access:,} households ({poor_access_percentage:.1f}%)"
        )

        if good_access_percentage >= 60:
            self.stdout.write(self.style.SUCCESS("  ✓ Good overall accessibility"))
        else:
            self.stdout.write(
                self.style.WARNING("  ⚠ Accessibility improvements needed")
            )
