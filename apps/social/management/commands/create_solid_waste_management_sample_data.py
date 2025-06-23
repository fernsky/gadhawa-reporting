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

        # Updated sample data representing actual solid waste management patterns by ward (including ward 8)
        solid_waste_management_data = [
            {
                "id": "d2c1f7ae-e445-4990-b5c9-f40fbeb5a0ed",
                "ward_number": 1,
                "solid_waste_management": "BURNING",
                "households": 830,
            },
            {
                "id": "66080f96-27f2-4472-9700-d18e90be1bfe",
                "ward_number": 1,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 66,
            },
            {
                "id": "93604dcb-6422-49f4-92cb-0f4ebc6fbefe",
                "ward_number": 1,
                "solid_waste_management": "DIGGING",
                "households": 668,
            },
            {
                "id": "71274897-d235-45a6-b67a-98feb74ce610",
                "ward_number": 1,
                "solid_waste_management": "HOME_COLLECTION",
                "households": 2,
            },
            {
                "id": "65d78d6e-49e2-46b2-a648-b202529e4a79",
                "ward_number": 1,
                "solid_waste_management": "RIVER",
                "households": 106,
            },
            {
                "id": "42177090-a20a-4aa7-89f0-1170c2c62a1f",
                "ward_number": 1,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 6,
            },
            {
                "id": "98cca696-c1dd-427b-b75c-ff2eca8675fe",
                "ward_number": 1,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 57,
            },
            {
                "id": "c0507dfe-d773-4b22-8bb7-e0c23a04053b",
                "ward_number": 2,
                "solid_waste_management": "BURNING",
                "households": 696,
            },
            {
                "id": "32dce89f-0bcd-43b8-9ed3-ebb01a4c5c98",
                "ward_number": 2,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 114,
            },
            {
                "id": "2f2b9ab6-cc98-46cd-9e9d-50a7ed83ff52",
                "ward_number": 2,
                "solid_waste_management": "DIGGING",
                "households": 60,
            },
            {
                "id": "7f7b7404-13ca-475d-b471-d008e2831e5f",
                "ward_number": 2,
                "solid_waste_management": "RIVER",
                "households": 37,
            },
            {
                "id": "122bcd6a-510e-478e-a0a9-aa54186ad64a",
                "ward_number": 2,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 1,
            },
            {
                "id": "dcd80072-0848-4a9c-9a6f-c902b21779f3",
                "ward_number": 2,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 293,
            },
            {
                "id": "0229d9ef-a650-465a-a893-7b2cf9bebdcb",
                "ward_number": 3,
                "solid_waste_management": "BURNING",
                "households": 872,
            },
            {
                "id": "b0a80976-c595-4376-8c11-4fc40651f3ca",
                "ward_number": 3,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 133,
            },
            {
                "id": "d3c850a7-aebc-4a5d-9a50-7ee1e23e3f50",
                "ward_number": 3,
                "solid_waste_management": "DIGGING",
                "households": 17,
            },
            {
                "id": "9178f0c7-89b9-4d25-9338-9b39231cddfb",
                "ward_number": 3,
                "solid_waste_management": "RIVER",
                "households": 216,
            },
            {
                "id": "b5a51555-8f0c-4ad5-bed4-894de028f21d",
                "ward_number": 3,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 1,
            },
            {
                "id": "5e189b1b-23e7-454c-8bf2-80bfe6b689f8",
                "ward_number": 3,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 55,
            },
            {
                "id": "3e60e035-1ca5-4b9e-8f08-e365d3ab25e5",
                "ward_number": 4,
                "solid_waste_management": "BURNING",
                "households": 821,
            },
            {
                "id": "69472163-2d16-462d-846a-77d779de9992",
                "ward_number": 4,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 35,
            },
            {
                "id": "28327246-d71f-4b00-84fe-868528d15865",
                "ward_number": 4,
                "solid_waste_management": "DIGGING",
                "households": 369,
            },
            {
                "id": "ec4b85b6-ff86-43ac-9b45-6d8adbb3c1f1",
                "ward_number": 4,
                "solid_waste_management": "RIVER",
                "households": 51,
            },
            {
                "id": "5aa29ab0-7559-4147-83ab-1a80a70e46c9",
                "ward_number": 4,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 9,
            },
            {
                "id": "b3836a78-a1fe-4ce0-b3c4-500fc6770a36",
                "ward_number": 4,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 15,
            },
            {
                "id": "1c978585-413a-4564-a26e-63d874d82f23",
                "ward_number": 5,
                "solid_waste_management": "BURNING",
                "households": 631,
            },
            {
                "id": "b5bf57e5-e5f4-47d8-927b-2be5c8888a82",
                "ward_number": 5,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 152,
            },
            {
                "id": "b4abe570-4438-4817-b25a-76345a4545ae",
                "ward_number": 5,
                "solid_waste_management": "DIGGING",
                "households": 614,
            },
            {
                "id": "92f3ec4a-83fd-4247-937b-192c599e4b23",
                "ward_number": 5,
                "solid_waste_management": "HOME_COLLECTION",
                "households": 1,
            },
            {
                "id": "18f02758-f148-40c6-9b50-032bef5b572c",
                "ward_number": 5,
                "solid_waste_management": "RIVER",
                "households": 50,
            },
            {
                "id": "d2b41cb8-e6b4-47d6-9bdd-fcd02abcfe20",
                "ward_number": 5,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 74,
            },
            {
                "id": "62326623-b2cc-4549-90a9-aca3d59f9d2b",
                "ward_number": 6,
                "solid_waste_management": "BURNING",
                "households": 808,
            },
            {
                "id": "2292760c-8fb3-4752-a4de-5d710760e553",
                "ward_number": 6,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 145,
            },
            {
                "id": "34603139-a590-4dda-a4fc-dfdb20780990",
                "ward_number": 6,
                "solid_waste_management": "DIGGING",
                "households": 305,
            },
            {
                "id": "f54d358f-4db3-477f-ab45-ace9d5e8fcb2",
                "ward_number": 6,
                "solid_waste_management": "HOME_COLLECTION",
                "households": 192,
            },
            {
                "id": "43844baa-38eb-42e9-ba25-cb84c030b3f4",
                "ward_number": 6,
                "solid_waste_management": "RIVER",
                "households": 59,
            },
            {
                "id": "f393c32f-ad2a-4f6a-a5f8-6a46e5c55dc1",
                "ward_number": 6,
                "solid_waste_management": "ROAD_OR_PUBLIC_PLACE",
                "households": 18,
            },
            {
                "id": "b7a62040-66e1-44f9-8969-0655d7f0dcc7",
                "ward_number": 6,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 234,
            },
            {
                "id": "959f786e-f896-4ad2-af76-9ee71b65bd52",
                "ward_number": 7,
                "solid_waste_management": "BURNING",
                "households": 152,
            },
            {
                "id": "7614d7f4-fd29-473d-b40e-c4d596889cd2",
                "ward_number": 7,
                "solid_waste_management": "COMPOST_MANURE",
                "households": 405,
            },
            {
                "id": "68c5268a-4941-4f53-81bf-97a012bcdadf",
                "ward_number": 7,
                "solid_waste_management": "DIGGING",
                "households": 118,
            },
            {
                "id": "80104f40-44b4-4a19-8013-0b146825e080",
                "ward_number": 7,
                "solid_waste_management": "HOME_COLLECTION",
                "households": 6,
            },
            {
                "id": "2052ac4a-fe47-4ee5-ba71-0aa7234970fa",
                "ward_number": 7,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 676,
            },
            {
                "id": "ddedec05-5e74-4e49-b1b2-f4dbcad4d598",
                "ward_number": 8,
                "solid_waste_management": "BURNING",
                "households": 60,
            },
            {
                "id": "370bf79e-1b10-4320-9aca-408ce4189716",
                "ward_number": 8,
                "solid_waste_management": "RIVER",
                "households": 66,
            },
            {
                "id": "0db4e581-882d-4ffd-a547-6f6af2819d4b",
                "ward_number": 8,
                "solid_waste_management": "WASTE_COLLECTING_PLACE",
                "households": 70,
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
        for ward_num in range(1, 9):
            ward_households = (
                WardWiseSolidWasteManagement.objects.filter(
                    ward_number=ward_num
                ).aggregate(total=models.Sum("households"))["total"]
                or 0
            )
            if ward_households > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_households:,} households")
