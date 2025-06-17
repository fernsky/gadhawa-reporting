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
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "road_status": "BLACKTOPPED",
                "households": 30,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "road_status": "EARTHEN",
                "households": 339,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "road_status": "NO_ROAD",
                "households": 642,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "road_status": "GRAVELED",
                "households": 33,
            },
            # Ward 2
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "road_status": "BLACKTOPPED",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "road_status": "EARTHEN",
                "households": 125,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "road_status": "NO_ROAD",
                "households": 810,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "road_status": "GRAVELED",
                "households": 2,
            },
            # Ward 3
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "road_status": "BLACKTOPPED",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "road_status": "EARTHEN",
                "households": 238,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "road_status": "NO_ROAD",
                "households": 398,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "road_status": "GRAVELED",
                "households": 2,
            },
            # Ward 4
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "road_status": "BLACKTOPPED",
                "households": 28,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "road_status": "EARTHEN",
                "households": 621,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "road_status": "NO_ROAD",
                "households": 199,
            },
            # Ward 5
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "road_status": "BLACKTOPPED",
                "households": 155,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "road_status": "EARTHEN",
                "households": 338,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "road_status": "NO_ROAD",
                "households": 220,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "road_status": "GRAVELED",
                "households": 6,
            },
            # Ward 6
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "road_status": "BLACKTOPPED",
                "households": 172,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "road_status": "EARTHEN",
                "households": 140,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "road_status": "NO_ROAD",
                "households": 548,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "road_status": "GRAVELED",
                "households": 4,
            },
            # Ward 7
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "road_status": "BLACKTOPPED",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "road_status": "EARTHEN",
                "households": 274,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "road_status": "NO_ROAD",
                "households": 312,
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
