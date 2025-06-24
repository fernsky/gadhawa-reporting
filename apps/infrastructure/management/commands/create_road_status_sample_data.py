"""
Management command to create road status infrastructure data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.infrastructure.models import WardWiseRoadStatus, RoadStatusChoice
import uuid


class Command(BaseCommand):
    help = (
        "Create road status infrastructure data based on actual municipality-wide data"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing road status data...")
            )
            WardWiseRoadStatus.objects.all().delete()

        self.stdout.write(
            "Creating road status infrastructure data based on actual municipality-wide data..."
        )

        # Sample data representing actual road status patterns by ward and type
        road_status_data = [
            # Ward 1
            {
                "id": "cb9c6a9a-5f89-4c4f-af77-79240815493f",
                "ward_number": 1,
                "road_status": "BLACK_TOPPED",
                "households": 425,
            },
            {
                "id": "2ccf66c6-aa53-4613-82e3-2772f0c27031",
                "ward_number": 1,
                "road_status": "DIRT",
                "households": 500,
            },
            {
                "id": "9908be0d-1ca0-4abc-bdf5-dc18d2b9b61a",
                "ward_number": 1,
                "road_status": "GORETO",
                "households": 217,
            },
            {
                "id": "148a0972-624e-4896-a14c-db5acc72828f",
                "ward_number": 1,
                "road_status": "GRAVELED",
                "households": 593,
            },
            # Ward 2
            {
                "id": "71a922f2-3252-46db-8305-698be4462fcb",
                "ward_number": 2,
                "road_status": "BLACK_TOPPED",
                "households": 569,
            },
            {
                "id": "2a8ecf64-80e6-4f72-b1ce-9b42290fa539",
                "ward_number": 2,
                "road_status": "DIRT",
                "households": 292,
            },
            {
                "id": "914d89b1-0ac9-464e-a40c-472486e06ce2",
                "ward_number": 2,
                "road_status": "GORETO",
                "households": 166,
            },
            {
                "id": "780c5b4b-b033-4a51-af78-a280566642f5",
                "ward_number": 2,
                "road_status": "GRAVELED",
                "households": 174,
            },
            # Ward 3
            {
                "id": "9da99979-e06e-48de-b700-5564e19fccda",
                "ward_number": 3,
                "road_status": "BLACK_TOPPED",
                "households": 392,
            },
            {
                "id": "ceda688f-f4d2-40b8-9e36-0f9cdd4ad43d",
                "ward_number": 3,
                "road_status": "DIRT",
                "households": 429,
            },
            {
                "id": "e593c0ba-f745-476d-b82b-7e3edd8cd69a",
                "ward_number": 3,
                "road_status": "GORETO",
                "households": 76,
            },
            {
                "id": "4db0d2ce-8eb5-4972-992d-5a4e2875d8e9",
                "ward_number": 3,
                "road_status": "GRAVELED",
                "households": 397,
            },
            # Ward 4
            {
                "id": "2f6fb8b1-063a-4a00-83b9-a5ed57a9e15f",
                "ward_number": 4,
                "road_status": "BLACK_TOPPED",
                "households": 181,
            },
            {
                "id": "0b42d3cd-3a52-444c-9c75-2f8fbd832da8",
                "ward_number": 4,
                "road_status": "DIRT",
                "households": 225,
            },
            {
                "id": "f6290268-202f-471b-9216-f3f25ae770a4",
                "ward_number": 4,
                "road_status": "GORETO",
                "households": 107,
            },
            {
                "id": "16980857-814f-442e-9aa2-779914808986",
                "ward_number": 4,
                "road_status": "GRAVELED",
                "households": 787,
            },
            # Ward 5
            {
                "id": "87892379-5cc8-43d2-a625-5305cedb0b3e",
                "ward_number": 5,
                "road_status": "BLACK_TOPPED",
                "households": 161,
            },
            {
                "id": "18124b7a-88ac-4812-8c3c-ad208351e1f5",
                "ward_number": 5,
                "road_status": "DIRT",
                "households": 170,
            },
            {
                "id": "dcf77f02-acf9-4931-83d7-4484db2e4581",
                "ward_number": 5,
                "road_status": "GORETO",
                "households": 108,
            },
            {
                "id": "111a5d04-7dcc-44f1-8ca4-8dea3032527b",
                "ward_number": 5,
                "road_status": "GRAVELED",
                "households": 1083,
            },
            # Ward 6
            {
                "id": "d253dead-733c-40b0-a686-c5de7c567561",
                "ward_number": 6,
                "road_status": "BLACK_TOPPED",
                "households": 539,
            },
            {
                "id": "26634929-e2ad-4d21-a54e-993b5ae65e8b",
                "ward_number": 6,
                "road_status": "DIRT",
                "households": 647,
            },
            {
                "id": "6e0a3907-4261-4c55-a9c4-6dc48d59e661",
                "ward_number": 6,
                "road_status": "GORETO",
                "households": 161,
            },
            {
                "id": "e407df63-23f9-40f0-9052-9939072ae737",
                "ward_number": 6,
                "road_status": "GRAVELED",
                "households": 414,
            },
            # Ward 7
            {
                "id": "65ee7db4-01fd-4d01-8c47-15b19819eb88",
                "ward_number": 7,
                "road_status": "BLACK_TOPPED",
                "households": 304,
            },
            {
                "id": "1a91e863-cfb3-4aff-95d1-27ba17062e74",
                "ward_number": 7,
                "road_status": "DIRT",
                "households": 409,
            },
            {
                "id": "f1bdc10d-43e1-4395-926d-f0279bcad3f9",
                "ward_number": 7,
                "road_status": "GORETO",
                "households": 278,
            },
            {
                "id": "706bd526-d3c4-4829-a5b9-8e8fd865609d",
                "ward_number": 7,
                "road_status": "GRAVELED",
                "households": 366,
            },
            # Ward 8
            {
                "id": "8e78e257-fc8f-4185-90d5-aa4c8e3d246b",
                "ward_number": 8,
                "road_status": "BLACK_TOPPED",
                "households": 115,
            },
            {
                "id": "bad19fd8-1c3c-4b02-b6a4-cd469db80321",
                "ward_number": 8,
                "road_status": "DIRT",
                "households": 75,
            },
            {
                "id": "b3acc8fe-5901-49b3-990c-55114da43d0c",
                "ward_number": 8,
                "road_status": "GRAVELED",
                "households": 6,
            },
        ]

        # Check if data already exists
        existing_count = WardWiseRoadStatus.objects.count()
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
            for data in road_status_data:
                obj, created = WardWiseRoadStatus.objects.get_or_create(
                    ward_number=data["ward_number"],
                    road_status=data["road_status"],
                    defaults={
                        "id": data["id"],
                        "households": data["households"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['road_status']} ({data['households']} households)"
                    )
                else:
                    # Update existing record
                    obj.households = data["households"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['road_status']} ({data['households']} households)"
                    )

        # Print summary
        total_records = WardWiseRoadStatus.objects.count()
        total_households = sum(
            WardWiseRoadStatus.objects.values_list("households", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(road_status_data)} road status infrastructure records "
                f"({created_count} new, {len(road_status_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total households covered: {total_households:,} households"
            )
        )

        # Print road status breakdown
        self.stdout.write("\nRoad status breakdown:")
        for road_choice in RoadStatusChoice.choices:
            road_code = road_choice[0]
            road_name = road_choice[1]
            road_households = (
                WardWiseRoadStatus.objects.filter(road_status=road_code).aggregate(
                    total=models.Sum("households")
                )["total"]
                or 0
            )

            if road_households > 0:
                percentage = road_households / total_households * 100
                self.stdout.write(
                    f"  {road_name}: {road_households:,} households ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {road_name}: 0 households (0.00%)")

        # Infrastructure impact analysis
        self.stdout.write("\nInfrastructure Impact Analysis:")

        # Quality road access
        quality_roads = ["BLACKTOPPED", "GRAVELED"]
        quality_households = sum(
            WardWiseRoadStatus.objects.filter(road_status=status).aggregate(
                total=models.Sum("households")
            )["total"]
            or 0
            for status in quality_roads
        )
        quality_percentage = (
            (quality_households / total_households * 100) if total_households > 0 else 0
        )

        self.stdout.write(
            f"  Quality road access: {quality_households:,} households ({quality_percentage:.1f}%)"
        )

        # Basic road access
        basic_households = (
            WardWiseRoadStatus.objects.filter(road_status="EARTHEN").aggregate(
                total=models.Sum("households")
            )["total"]
            or 0
        )
        basic_percentage = (
            (basic_households / total_households * 100) if total_households > 0 else 0
        )

        self.stdout.write(
            f"  Basic road access: {basic_households:,} households ({basic_percentage:.1f}%)"
        )

        # No road access
        no_road_households = (
            WardWiseRoadStatus.objects.filter(road_status="NO_ROAD").aggregate(
                total=models.Sum("households")
            )["total"]
            or 0
        )
        no_road_percentage = (
            (no_road_households / total_households * 100) if total_households > 0 else 0
        )

        self.stdout.write(
            f"  No road access: {no_road_households:,} households ({no_road_percentage:.1f}%)"
        )

        # Ward-wise summary
        self.stdout.write("\nWard-wise road infrastructure summary:")
        for ward_num in range(1, 8):
            ward_households = (
                WardWiseRoadStatus.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("households")
                )["total"]
                or 0
            )
            if ward_households > 0:
                # Calculate quality road percentage for this ward
                ward_quality = sum(
                    WardWiseRoadStatus.objects.filter(
                        ward_number=ward_num, road_status=status
                    ).aggregate(total=models.Sum("households"))["total"]
                    or 0
                    for status in quality_roads
                )
                ward_quality_percentage = (
                    (ward_quality / ward_households * 100) if ward_households > 0 else 0
                )

                self.stdout.write(
                    f"  वडा {ward_num}: {ward_households:,} households "
                    f"(Quality roads: {ward_quality_percentage:.1f}%)"
                )

        # Critical infrastructure insights
        self.stdout.write("\nCritical Infrastructure Insights:")

        if no_road_percentage > 40:
            self.stdout.write(
                "  🚧 CRITICAL: Over 40% households lack road access - urgent infrastructure development needed"
            )

        if quality_percentage < 20:
            self.stdout.write(
                "  🛣️  Low quality road access - road improvement programs needed"
            )

        if basic_percentage > 50:
            self.stdout.write(
                "  🔧 High dependency on earthen roads - road upgrading opportunities exist"
            )

        # Best and worst performing wards
        ward_performance = []
        for ward_num in range(1, 8):
            ward_households = (
                WardWiseRoadStatus.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("households")
                )["total"]
                or 0
            )

            if ward_households > 0:
                ward_quality = sum(
                    WardWiseRoadStatus.objects.filter(
                        ward_number=ward_num, road_status=status
                    ).aggregate(total=models.Sum("households"))["total"]
                    or 0
                    for status in quality_roads
                )
                ward_quality_percentage = (
                    (ward_quality / ward_households * 100) if ward_households > 0 else 0
                )
                ward_performance.append((ward_num, ward_quality_percentage))

        if ward_performance:
            best_ward = max(ward_performance, key=lambda x: x[1])
            worst_ward = min(ward_performance, key=lambda x: x[1])

            self.stdout.write(
                f"\n🏆 Best road infrastructure: वडा {best_ward[0]} ({best_ward[1]:.1f}% quality roads)"
            )
            self.stdout.write(
                f"⚠️  Needs improvement: वडा {worst_ward[0]} ({worst_ward[1]:.1f}% quality roads)"
            )

        self.stdout.write(
            f"\n📊 Overall road infrastructure analysis shows {total_households:,} households"
        )
        self.stdout.write(
            "🎯 Focus areas: Road construction, upgrading earthen roads, and connectivity improvement"
        )
