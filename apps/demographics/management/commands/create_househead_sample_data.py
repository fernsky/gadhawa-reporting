"""
Management command to create househead demographics data based on actual data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models
from apps.demographics.models import WardWiseHouseheadGender, GenderChoice
import uuid


class Command(BaseCommand):
    help = "Create househead demographics data based on actual municipality-wide data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing househead data..."))
            WardWiseHouseheadGender.objects.all().delete()

        self.stdout.write(
            "Creating househead demographics data based on actual municipality-wide data..."
        )

        # New househead data (wards 1-8, all genders, with provided IDs)
        raw_househead_data = [
            {
                "id": "2ca16b42-0c4a-4053-bb09-2dad23b40c10",
                "ward_number": 1,
                "ward_name": None,
                "gender": "MALE",
                "population": 389,
            },
            {
                "id": "9b434509-d8d1-4127-9658-1555e74d3c45",
                "ward_number": 1,
                "ward_name": None,
                "gender": "FEMALE",
                "population": 703,
            },
            {
                "id": "ab30f2df-cdb9-4252-ab94-505cf3bf7a4a",
                "ward_number": 2,
                "ward_name": None,
                "gender": "OTHER",
                "population": 4,
            },
            {
                "id": "5e4bd4eb-d590-4bc2-8336-c6dc2584941a",
                "ward_number": 2,
                "ward_name": None,
                "gender": "MALE",
                "population": 381,
            },
            {
                "id": "8ce0ea1d-e535-4a76-8f76-8b39a182f9ea",
                "ward_number": 2,
                "ward_name": None,
                "gender": "FEMALE",
                "population": 465,
            },
            {
                "id": "77224678-41ac-4d9c-bc83-b4dd09f20424",
                "ward_number": 3,
                "ward_name": None,
                "gender": "MALE",
                "population": 393,
            },
            {
                "id": "ed29632b-61fc-40cc-8a1f-1779dbb01a20",
                "ward_number": 3,
                "ward_name": None,
                "gender": "FEMALE",
                "population": 633,
            },
            {
                "id": "277f59c7-2f86-4c3a-bd93-ae5c007b39e3",
                "ward_number": 4,
                "ward_name": None,
                "gender": "OTHER",
                "population": 56,
            },
            {
                "id": "1360f870-4f75-4e34-aac2-dccf00eed2ba",
                "ward_number": 4,
                "ward_name": None,
                "gender": "MALE",
                "population": 395,
            },
            {
                "id": "0d08b256-6cda-4a21-a76c-2c68b4bb59a7",
                "ward_number": 4,
                "ward_name": None,
                "gender": "FEMALE",
                "population": 423,
            },
            {
                "id": "22644f0a-ef2a-4017-92ec-c8ace057a599",
                "ward_number": 5,
                "ward_name": None,
                "gender": "OTHER",
                "population": 388,
            },
            {
                "id": "9a9adb10-ccfb-4290-8a16-2fdac5723a06",
                "ward_number": 5,
                "ward_name": None,
                "gender": "MALE",
                "population": 470,
            },
            {
                "id": "96551f89-aac3-4339-a8b2-9a7aeae7774d",
                "ward_number": 5,
                "ward_name": None,
                "gender": "FEMALE",
                "population": 524,
            },
            {
                "id": "ad01e877-8630-41e1-a51c-77184a148bfd",
                "ward_number": 6,
                "ward_name": None,
                "gender": "OTHER",
                "population": 126,
            },
            {
                "id": "4c43a64d-ace3-43d9-aa79-9f07e77b5f2b",
                "ward_number": 6,
                "ward_name": None,
                "gender": "MALE",
                "population": 806,
            },
            {
                "id": "93491d8a-dbc0-4df3-9128-494a168ff476",
                "ward_number": 6,
                "ward_name": None,
                "gender": "FEMALE",
                "population": 562,
            },
            {
                "id": "a859ed63-37cf-4d4e-806f-c7ecedd8c0c1",
                "ward_number": 7,
                "ward_name": None,
                "gender": "OTHER",
                "population": 124,
            },
            {
                "id": "156fe52a-71a5-4484-9e8c-bf69fde9ef15",
                "ward_number": 7,
                "ward_name": None,
                "gender": "MALE",
                "population": 637,
            },
            {
                "id": "c59d4b21-0336-4846-af8d-436c6b12a47e",
                "ward_number": 7,
                "ward_name": None,
                "gender": "FEMALE",
                "population": 301,
            },
            {
                "id": "386927ca-4e98-4e74-a4e3-2bc7607c7cbb",
                "ward_number": 8,
                "ward_name": None,
                "gender": "MALE",
                "population": 31,
            },
            {
                "id": "dd392f0d-5786-4e51-bdad-93cb2fe61e15",
                "ward_number": 8,
                "ward_name": None,
                "gender": "FEMALE",
                "population": 54,
            },
        ]

        # Set ward_name if missing
        ward_name_map = {i: f"वडा नं. {i}" for i in range(1, 9)}
        for entry in raw_househead_data:
            if not entry["ward_name"]:
                entry["ward_name"] = ward_name_map.get(
                    entry["ward_number"], f"वडा नं. {entry['ward_number']}"
                )

        self.stdout.write(
            f"Processing {len(raw_househead_data)} records for househead demographics..."
        )

        existing_count = WardWiseHouseheadGender.objects.count()
        if existing_count > 0 and not options["clear"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_count} existing records. Use --clear to replace them."
                )
            )
            return

        created_count = 0
        with transaction.atomic():
            for data in raw_househead_data:
                obj, created = WardWiseHouseheadGender.objects.get_or_create(
                    ward_number=data["ward_number"],
                    gender=data["gender"],
                    defaults={
                        "id": data["id"],
                        "ward_name": data["ward_name"],
                        "population": data["population"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f"Created: Ward {data['ward_number']} - {data['gender']} ({data['population']} households)"
                    )
                else:
                    obj.population = data["population"]
                    obj.ward_name = data["ward_name"]
                    obj.save()
                    self.stdout.write(
                        f"Updated: Ward {data['ward_number']} - {data['gender']} ({data['population']} households)"
                    )

        total_records = WardWiseHouseheadGender.objects.count()
        total_households = sum(
            WardWiseHouseheadGender.objects.values_list("population", flat=True)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {len(raw_househead_data)} househead demographic records "
                f"({created_count} new, {len(raw_househead_data) - created_count} updated)\n"
                f"Total records in database: {total_records}\n"
                f"Total households covered: {total_households:,} households"
            )
        )

        # Calculate and display gender-wise summary
        self.stdout.write("\nHousehead gender breakdown:")
        gender_totals = {}
        for gender_choice in GenderChoice.choices:
            gender_code = gender_choice[0]
            gender_name = gender_choice[1]
            gender_households = (
                WardWiseHouseheadGender.objects.filter(gender=gender_code).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            gender_totals[gender_code] = gender_households

            if gender_households > 0:
                percentage = gender_households / total_households * 100
                self.stdout.write(
                    f"  {gender_name}: {gender_households:,} households ({percentage:.2f}%)"
                )
            else:
                self.stdout.write(f"  {gender_name}: 0 households (0.00%)")

        # Ward-wise summary
        self.stdout.write("\nWard-wise household summary:")
        for ward_num in range(1, 9):  # Now covering wards 1-8
            ward_households = (
                WardWiseHouseheadGender.objects.filter(ward_number=ward_num).aggregate(
                    total=models.Sum("population")
                )["total"]
                or 0
            )
            if ward_households > 0:
                self.stdout.write(f"  वडा {ward_num}: {ward_households:,} households")
