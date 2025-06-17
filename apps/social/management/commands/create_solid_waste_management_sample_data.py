"""
Management command to create solid waste management social data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.social.models import WardWiseSolidWasteManagement, SolidWasteManagementChoice
import uuid


class Command(BaseCommand):
    help = "Create solid waste management social data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(
                self.style.WARNING("Clearing existing solid waste management data...")
            )
            WardWiseSolidWasteManagement.objects.all().delete()

        self.stdout.write(
            "Creating solid waste management social data based on actual municipality-wide data..."
        )

        # Sample data representing actual solid waste management patterns by ward
        solid_waste_management_data = [
            # Ward 1
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "solid_waste_management": "BURNING",
                "households": 72,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 880,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "solid_waste_management": "DIGGING",
                "households": 6,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "solid_waste_management": "HOME_COLLECTION",
                "households": 5,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "solid_waste_management": "RIVER",
                "households": 52,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 2,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 1,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 122,
            },
            # Ward 2
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "solid_waste_management": "BURNING",
                "households": 319,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 133,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "solid_waste_management": "DIGGING",
                "households": 114,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "solid_waste_management": "HOME_COLLECTION",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "solid_waste_management": "RIVER",
                "households": 244,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 3,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 2,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 104,
            },
            # Ward 3
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "solid_waste_management": "BURNING",
                "households": 98,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 410,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "solid_waste_management": "DIGGING",
                "households": 6,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "solid_waste_management": "HOME_COLLECTION",
                "households": 2,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "solid_waste_management": "RIVER",
                "households": 39,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 5,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 3,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 4,
            },
            # Ward 4
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "solid_waste_management": "BURNING",
                "households": 141,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 592,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "solid_waste_management": "DIGGING",
                "households": 73,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "solid_waste_management": "RIVER",
                "households": 25,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 6,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 4,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 11,
            },
            # Ward 5
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "solid_waste_management": "BURNING",
                "households": 67,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 130,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "solid_waste_management": "DIGGING",
                "households": 204,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "solid_waste_management": "RIVER",
                "households": 123,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 5,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 195,
            },
            # Ward 6
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "solid_waste_management": "BURNING",
                "households": 67,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 563,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "solid_waste_management": "DIGGING",
                "households": 89,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "solid_waste_management": "HOME_COLLECTION",
                "households": 5,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "solid_waste_management": "RIVER",
                "households": 86,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 1,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 6,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 53,
            },
            # Ward 7
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "solid_waste_management": "BURNING",
                "households": 361,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 54,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "solid_waste_management": "DIGGING",
                "households": 57,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "solid_waste_management": "RIVER",
                "households": 107,
            },
            {
                "id": str(uuid.uuid4()),
                "ward_number": 7,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 8,
            },
        ]

        # Check if data already exists
        existing_count = WardWiseSolidWasteManagement.objects.count()
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
            for data in solid_waste_management_data:
                obj, created = WardWiseSolidWasteManagement.objects.get_or_create(
                    ward_number=data["ward_number"],
                    solid_waste_management=data["solid_waste_management"],
                    defaults={
                        "id": data["id"],
                        "households": data["households"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['solid_waste_management']} ({data['households']} households)"
                    )
                else:
                    # Update existing record
                    obj.households = data["households"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['solid_waste_management']} ({data['households']} households)"
                    )

        # Print summary
        total_records = WardWiseSolidWasteManagement.objects.count()
        total_households = sum(
            WardWiseSolidWasteManagement.objects.values_list("households", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(solid_waste_management_data)} solid waste management social records "
                f"({created_count} new, {len(solid_waste_management_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total households covered: {total_households:,} households"
            )
        )

        # Print waste management method breakdown
        self.stdout.write("\nSolid waste management method breakdown:")
        for waste_choice in SolidWasteManagementChoice.choices:
            waste_code = waste_choice[0]
            waste_name = waste_choice[1]
            waste_households = (
                WardWiseSolidWasteManagement.objects.filter(
                    solid_waste_management=waste_code
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )

            if waste_households > 0:
                percentage = waste_households / total_households * 100
                self.stdout.write(
                    f"  {waste_name}: {waste_households:,} households ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {waste_name}: 0 households (0.00%)")

        # Environmental impact analysis
        self.stdout.write("\nEnvironmental Impact Analysis:")
        eco_friendly_methods = [
            "COMPOST_MANURE",
            "HOME_COLLECTION",
            "WASTE_COLLECTING_PLACE",
        ]
        harmful_methods = ["BURNING", "RIVER", "ROAD_OR_PUBLIC_PLACE"]

        eco_friendly_households = sum(
            WardWiseSolidWasteManagement.objects.filter(
                solid_waste_management=method
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
            for method in eco_friendly_methods
        )

        harmful_households = sum(
            WardWiseSolidWasteManagement.objects.filter(
                solid_waste_management=method
            ).aggregate(total=models.Sum("households"))["total"]
            or 0
            for method in harmful_methods
        )

        eco_percentage = (
            (eco_friendly_households / total_households * 100)
            if total_households > 0
            else 0
        )
        harmful_percentage = (
            (harmful_households / total_households * 100) if total_households > 0 else 0
        )

        self.stdout.write(
            f"  Eco-friendly methods: {eco_friendly_households:,} households ({eco_percentage:.1f}%)"
        )
        self.stdout.write(
            f"  Environmentally harmful methods: {harmful_households:,} households ({harmful_percentage:.1f}%)"
        )

        # Ward-wise summary
        self.stdout.write("\nWard-wise solid waste management summary:")
        for ward_num in range(1, 8):
            ward_households = (
                WardWiseSolidWasteManagement.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )
            if ward_households > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_households:,} households")
